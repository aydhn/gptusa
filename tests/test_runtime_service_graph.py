import pytest
from usa_signal_bot.runtime_service_graph.runtime_registry_ingestion import ingest_runtime_registry_review_payload
from usa_signal_bot.runtime_service_graph.service_catalog import default_runtime_service_catalog
from usa_signal_bot.runtime_service_graph.dependency_contracts import build_default_dependency_contracts
from usa_signal_bot.runtime_service_graph.dependency_graph import build_runtime_service_edges
from usa_signal_bot.runtime_service_graph.dependency_cycle_detector import detect_dependency_cycles
from usa_signal_bot.runtime_service_graph.dependency_contract_validator import validate_all_dependency_contracts
from usa_signal_bot.runtime_service_graph.service_graph_builder import build_runtime_service_graph
from usa_signal_bot.runtime_service_graph.safe_orchestration_shell import SafeExecutionOrchestrationShell
from usa_signal_bot.runtime_service_graph.service_graph_report import build_runtime_service_graph_full_review

def test_ingestion():
    payload = {"normalized_registry": {}, "safety_policy_valid": True, "registry_normalized": True}
    res = ingest_runtime_registry_review_payload(payload)
    assert res.valid_for_phase103 is True

def test_catalog():
    nodes = default_runtime_service_catalog()
    assert len(nodes) > 0

def test_contracts():
    nodes = default_runtime_service_catalog()
    contracts = build_default_dependency_contracts(nodes)
    assert len(contracts) > 0
    errors = validate_all_dependency_contracts(contracts)
    assert len(errors) == 0

def test_cycles():
    nodes = default_runtime_service_catalog()
    contracts = build_default_dependency_contracts(nodes)
    edges = build_runtime_service_edges(nodes, contracts)
    cycles = detect_dependency_cycles(edges)
    assert len(cycles) == 0

def test_builder():
    graph = build_runtime_service_graph()
    assert graph.graph_valid is True

def test_shell():
    graph = build_runtime_service_graph()
    shell = SafeExecutionOrchestrationShell(graph)
    plan = shell.build_plan()
    assert plan.dry_run_only is True
    res = shell.dry_run(plan)
    assert res.execution_performed is False
    assert res.passed is True

def test_report():
    rev = build_runtime_service_graph_full_review()
    assert rev.service_graph.graph_valid is True
    assert rev.dry_run_result.passed is True
