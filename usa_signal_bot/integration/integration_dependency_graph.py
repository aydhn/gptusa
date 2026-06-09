
from typing import Any, Dict, List
import hashlib

from usa_signal_bot.integration.phase158_models import IntegrationDependencyGraph, SystemArtifactInventory, IntegrationDependencyEdge
from usa_signal_bot.core.enums import IntegrationDependencyKind

def build_integration_dependency_graph(inventory: SystemArtifactInventory) -> IntegrationDependencyGraph:
    graph = IntegrationDependencyGraph()
    graph.nodes = inventory.artifacts
    graph.node_count = len(graph.nodes)
    graph.edges = build_default_dependency_edges(inventory)
    graph.edge_count = len(graph.edges)

    graph.cyclic_dependency_detected = detect_integration_dependency_cycles(graph)
    graph.graph_hash = compute_integration_dependency_graph_hash(graph)
    graph.graph_valid = len(validate_integration_dependency_graph(graph)) == 0
    return graph

def build_default_dependency_edges(inventory: SystemArtifactInventory) -> List[IntegrationDependencyEdge]:
    edges = []
    nodes = {n.artifact_name: n for n in inventory.artifacts}

    chain = [
        "CONFIG", "DATA_PROVIDER", "FEATURE_ENGINE", "REGIME_ENGINE",
        "ML_GOVERNANCE", "BACKTEST_CLOSURE", "PORTFOLIO_FOUNDATION",
        "SIZING_PROTOTYPE", "ALLOCATION_SANDBOX", "OPTIMIZER_SANDBOX",
        "PORTFOLIO_RISK_REPORTING"
    ]

    for i in range(len(chain) - 1):
        if chain[i] in nodes and chain[i+1] in nodes:
            edges.append(IntegrationDependencyEdge(
                source_artifact_id=nodes[chain[i]].artifact_id,
                target_artifact_id=nodes[chain[i+1]].artifact_id,
                dependency_kind=IntegrationDependencyKind.REQUIRES,
                required=True,
                valid=True
            ))
    return edges

def compute_integration_dependency_graph_hash(graph: IntegrationDependencyGraph) -> str:
    h = hashlib.sha256()
    for edge in graph.edges:
        h.update((edge.source_artifact_id + edge.target_artifact_id).encode('utf-8'))
    return h.hexdigest()

def detect_integration_dependency_cycles(graph: IntegrationDependencyGraph) -> bool:
    # Simplified cycle detection for a linear chain
    # In a full implementation, you'd use a graph traversal algorithm like Tarjan's or DFS
    return False

def validate_integration_dependency_graph(graph: IntegrationDependencyGraph) -> List[str]:
    violations = []
    if graph.cyclic_dependency_detected:
        violations.append("Cyclic dependencies detected in the integration graph.")
    return violations

def integration_dependency_graph_summary(graph: IntegrationDependencyGraph) -> Dict[str, Any]:
    return {
        "nodes": graph.node_count,
        "edges": graph.edge_count,
        "cyclic": graph.cyclic_dependency_detected,
        "valid": graph.graph_valid
    }

def integration_dependency_graph_to_text(graph: IntegrationDependencyGraph, limit: int = 300) -> str:
    summary = integration_dependency_graph_summary(graph)
    text = f"Dependency Graph: {summary}"
    return text[:limit] + "..." if len(text) > limit else text
