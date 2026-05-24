from typing import Any, Dict
from usa_signal_bot.runtime_service_graph.phase103_models import (
    RuntimeRegistryIngestionResult,
    RuntimeServiceNode,
    RuntimeServiceEdge,
    DependencyContract,
    RuntimeServiceGraph,
    OrchestrationStep,
    SafeOrchestrationPlan,
    OrchestrationDryRunResult,
    RuntimeServiceGraphFullReview
)

def runtime_registry_ingestion_result_to_text(item: RuntimeRegistryIngestionResult) -> str:
    return f"Ingest {item.ingestion_id} - valid={item.valid_for_phase103}"

def runtime_service_node_to_text(item: RuntimeServiceNode) -> str:
    return f"Node {item.service_id}"

def runtime_service_edge_to_text(item: RuntimeServiceEdge) -> str:
    return f"Edge {item.source_service_id}->{item.target_service_id}"

def dependency_contract_to_text(item: DependencyContract) -> str:
    return f"Contract {item.contract_id}"

def runtime_service_graph_to_text(item: RuntimeServiceGraph, limit: int = 300) -> str:
    return f"Graph {item.graph_id} - valid={item.graph_valid}"

def orchestration_step_to_text(item: OrchestrationStep) -> str:
    return f"Step {item.step_id}"

def safe_orchestration_plan_to_text(item: SafeOrchestrationPlan, limit: int = 300) -> str:
    return f"Plan {item.plan_id}"

def orchestration_dry_run_result_to_text(item: OrchestrationDryRunResult) -> str:
    return f"Result {item.result_id} - passed={item.passed}"

def runtime_service_graph_full_review_to_text(item: RuntimeServiceGraphFullReview, limit: int = 300) -> str:
    return f"Review {item.review_id}"

def service_graph_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Store: {summary.get('graphs', 0)} graphs, {summary.get('reviews', 0)} reviews"

def runtime_service_graph_limitations_text() -> str:
    return "Phase 103 does not enable paper trading, broker execution, or real telegram sends."
