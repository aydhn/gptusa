import pytest
from pathlib import Path
from usa_signal_bot.risk.risk_store import (
    risk_store_dir,
    build_risk_run_dir,
    write_risk_run_result_json,
    read_risk_run_result_json,
    write_risk_decisions_jsonl,
    read_risk_decisions_jsonl
)
from usa_signal_bot.risk.risk_models import RiskRunResult, RiskDecision
from usa_signal_bot.core.enums import RiskRunStatus, RiskDecisionStatus, SignalAction, PositionSizingMethod, RiskSeverity

def test_risk_store_paths(tmp_path):
    d = risk_store_dir(tmp_path)
    assert d.exists()
    rd = build_risk_run_dir(tmp_path, "run123")
    assert rd.exists()
    assert rd.name == "run123"

def test_risk_run_write_read(tmp_path):
    rd = build_risk_run_dir(tmp_path, "run123")
    run = RiskRunResult("run123", "2023-01-01T00:00:00Z", RiskRunStatus.COMPLETED, 0, 0, 0, 0, 0, [], [], [])
    write_risk_run_result_json(rd, run)
    res = read_risk_run_result_json(rd)
    assert res["run_id"] == "run123"

def test_risk_decisions_write_read(tmp_path):
    rd = build_risk_run_dir(tmp_path, "run123")
    dec = RiskDecision("d1", "c1", "s1", "AAPL", "strat", "1d", RiskDecisionStatus.APPROVED, SignalAction.LONG, 10, 1000, PositionSizingMethod.FIXED_NOTIONAL, [], [], 10.0, RiskSeverity.INFO, [], "2023-01-01T00:00:00Z")
    write_risk_decisions_jsonl(rd, [dec])
    res = read_risk_decisions_jsonl(rd)
    assert len(res) == 1
    assert res[0]["decision_id"] == "d1"
