import pytest
from usa_signal_bot.research_execution.config_snapshot import build_baseline_config_snapshot
from usa_signal_bot.research_execution.run_context import build_baseline_run_context

def test_build_baseline_run_context_enforces_safety():
    plan = {"experiment_id": "exp_1", "validation_plan": {"data_scope": {"symbols": ["AAPL"]}}}
    snap = build_baseline_config_snapshot({"a": 1})

    ctx = build_baseline_run_context(plan, snap)
    assert ctx.allowed_to_modify_config is False
    assert ctx.allowed_to_send_orders is False
