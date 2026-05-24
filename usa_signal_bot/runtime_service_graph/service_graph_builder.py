from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from usa_signal_bot.runtime_service_graph.phase103_models import (
    RuntimeServiceGraph,
    RuntimeRegistryIngestionResult,
    create_runtime_service_graph_id
)
from usa_signal_bot.core.enums import RuntimeServiceGraphStatus, RuntimeServiceGraphDecision, RuntimeServiceGraphRiskFlag
from usa_signal_bot.runtime_service_graph.service_catalog import default_runtime_service_catalog
from usa_signal_bot.runtime_service_graph.dependency_contracts import build_default_dependency_contracts
from usa_signal_bot.runtime_service_graph.dependency_graph import build_runtime_service_edges, find_missing_dependencies
from usa_signal_bot.runtime_service_graph.dependency_cycle_detector import dependency_graph_has_cycles
from usa_signal_bot.runtime_service_graph.dependency_contract_validator import validate_all_dependency_contracts

def build_runtime_service_graph(registry_ingestion: Optional[RuntimeRegistryIngestionResult] = None) -> RuntimeServiceGraph:
    nodes = default_runtime_service_catalog()
    contracts = build_default_dependency_contracts(nodes)
    edges = build_runtime_service_edges(nodes, contracts)

    missing = find_missing_dependencies(nodes, edges)
    cycles = dependency_graph_has_cycles(edges)
    contract_errors = validate_all_dependency_contracts(contracts)

    graph_valid = len(missing) == 0 and not cycles and len(contract_errors) == 0

    if registry_ingestion and not registry_ingestion.valid_for_phase103:
        graph_valid = False

    return RuntimeServiceGraph(
        graph_id=create_runtime_service_graph_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=RuntimeServiceGraphStatus.VALIDATED if graph_valid else RuntimeServiceGraphStatus.FAILED,
        decision=RuntimeServiceGraphDecision.CREATE_SERVICE_GRAPH if graph_valid else RuntimeServiceGraphDecision.BLOCK,
        source_runtime_registry_review_id=registry_ingestion.source_review_id if registry_ingestion else None,
        nodes=nodes,
        edges=edges,
        dependency_contracts=contracts,
        graph_has_cycles=cycles,
        missing_dependency_count=len(missing),
        invalid_contract_count=len(contract_errors),
        blocked_route_count=0,
        provider_nodes_ready=True,
        core_nodes_ready=True,
        graph_valid=graph_valid,
        activation_allowed=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        scraping_enabled=False,
        dashboard_enabled=False,
        risk_flags=[],
        warnings=[],
        errors=missing + contract_errors,
        metadata={}
    )

def build_default_runtime_service_graph() -> RuntimeServiceGraph:
    return build_runtime_service_graph()

def validate_runtime_service_graph_safety(graph: RuntimeServiceGraph) -> List[str]:
    errors = []
    if graph.activation_allowed:
        errors.append("Graph permits activation")
    if graph.active_paper_enabled:
        errors.append("Graph permits active paper")
    if graph.broker_execution_enabled:
        errors.append("Graph permits broker execution")
    if graph.paper_state_mutation_enabled:
        errors.append("Graph permits paper mutation")
    if graph.telegram_real_send_enabled:
        errors.append("Graph permits telegram sends")
    if graph.scraping_enabled:
        errors.append("Graph permits scraping")
    if graph.dashboard_enabled:
        errors.append("Graph permits dashboard")
    return errors

def runtime_service_graph_summary(graph: RuntimeServiceGraph) -> Dict[str, Any]:
    return {
        "valid": graph.graph_valid,
        "nodes": len(graph.nodes),
        "edges": len(graph.edges)
    }

def runtime_service_graph_to_text(graph: RuntimeServiceGraph, limit: int = 300) -> str:
    return f"Service graph {graph.graph_id} valid: {graph.graph_valid}"
