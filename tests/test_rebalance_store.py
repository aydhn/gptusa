import pytest
import json
from pathlib import Path
from usa_signal_bot.portfolio_rebalance.rebalance_models import (
    CurrentPortfolioState, TargetPortfolioState, DriftMeasurement,
    RebalanceAction, RebalancePlan, RebalanceReview
)
from usa_signal_bot.core.enums import RebalanceMode, RebalanceStatus, RebalanceReportType, RebalanceActionType, DriftType, DriftSeverity
from usa_signal_bot.portfolio_rebalance.rebalance_store import (
    rebalance_store_dir, write_current_portfolio_state_json,
    write_target_portfolio_state_json, write_drift_measurements_jsonl,
    write_rebalance_actions_jsonl, write_rebalance_plan_json,
    write_rebalance_review_json, read_rebalance_review_json,
    list_rebalance_reviews, get_latest_rebalance_review,
    rebalance_store_summary
)

def test_rebalance_store(tmp_path):
    # Setup objects
    curr = CurrentPortfolioState("1", "now", 1000, 1000)
    tgt = TargetPortfolioState("2", "now", 1000, 1000)
    drift = DriftMeasurement("d", "now", DriftType.SYMBOL_WEIGHT, "AAPL", DriftSeverity.NONE)
    action = RebalanceAction("a", "AAPL", RebalanceActionType.HOLD, RebalanceStatus.NOT_NEEDED)
    plan = RebalancePlan("p", "now", RebalanceMode.HYBRID, RebalanceStatus.NOT_NEEDED, 0, 0, 0)
    review = RebalanceReview("r", "now", RebalanceReportType.FULL_REBALANCE_REVIEW, plan)

    # Write
    curr_file = tmp_path / "curr.json"
    tgt_file = tmp_path / "tgt.json"
    drifts_file = tmp_path / "drifts.jsonl"
    acts_file = tmp_path / "acts.jsonl"
    plan_file = tmp_path / "plan.json"
    rev_file = tmp_path / "rev.json"

    write_current_portfolio_state_json(curr_file, curr)
    write_target_portfolio_state_json(tgt_file, tgt)
    write_drift_measurements_jsonl(drifts_file, [drift])
    write_rebalance_actions_jsonl(acts_file, [action])
    write_rebalance_plan_json(plan_file, plan)
    write_rebalance_review_json(rev_file, review)

    assert curr_file.exists()
    assert tgt_file.exists()
    assert drifts_file.exists()
    assert acts_file.exists()
    assert plan_file.exists()
    assert rev_file.exists()

    # Read review
    data = read_rebalance_review_json(rev_file)
    assert data["review_id"] == "r"

    # Store dirs
    store_dir = rebalance_store_dir(tmp_path)
    assert store_dir.exists()
