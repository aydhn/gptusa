import pytest
from usa_signal_bot.research_execution.plan_loader import load_experiment_plan_from_dict

def test_plan_loader_blocks_auto_execution():
    payload = {
        "experiment_id": "exp_1",
        "allowed_for_auto_execution": True
    }
    res = load_experiment_plan_from_dict(payload)
    assert any("BLOCKED" in w for w in res["warnings"])

def test_plan_loader_warns_missing_id():
    payload = {}
    res = load_experiment_plan_from_dict(payload)
    assert any("Missing experiment_id" in w for w in res["warnings"])
