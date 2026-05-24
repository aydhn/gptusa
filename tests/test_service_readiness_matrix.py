import pytest
from usa_signal_bot.runtime_lifecycle.service_readiness_matrix import build_service_readiness_matrix
from usa_signal_bot.runtime_lifecycle.config_readiness_validator import validate_config_readiness
from usa_signal_bot.runtime_lifecycle.no_execution_readiness_validator import validate_no_execution_readiness
from usa_signal_bot.runtime_lifecycle.readiness_gate_builder import build_readiness_gate
from usa_signal_bot.runtime_lifecycle.readiness_gate_evaluator import evaluate_readiness_gate
from usa_signal_bot.runtime_lifecycle.startup_check_runner import StartupCheckRunner
from usa_signal_bot.core.enums import ReadinessGateDecision

def test_service_readiness_matrix_builds():
    payload = {"runtime_service_graph": {"nodes": [{"service_id": "s1"}, {"service_id": "s2"}]}}
    matrix = build_service_readiness_matrix(payload)
    assert matrix.total_services == 2
    assert matrix.ready_services == 2
    assert matrix.no_execution_ready is True

def test_config_readiness_blocks_execution():
    errors = validate_config_readiness({"allow_active_paper": True})
    assert len(errors) > 0
    assert "Config allows active paper" in errors

def test_no_execution_readiness_blocks_active():
    errors = validate_no_execution_readiness()
    assert len(errors) == 0

def test_readiness_gate_flow():
    runner = StartupCheckRunner()
    report = runner.run_all_checks()
    matrix = build_service_readiness_matrix()

    gate = build_readiness_gate(report, matrix)
    decision = evaluate_readiness_gate(gate)

    assert gate.activation_allowed is False
    assert gate.broker_execution_enabled is False
    assert decision == ReadinessGateDecision.PASS_TO_PHASE105_CORE_ACCEPTANCE
    assert gate.metadata_only is True
