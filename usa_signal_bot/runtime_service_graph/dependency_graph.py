from typing import Any, Dict, List
from usa_signal_bot.runtime_service_graph.phase103_models import (
    RuntimeServiceNode,
    RuntimeServiceEdge,
    DependencyContract,
    create_edge_id
)

def build_runtime_service_edges(nodes: List[RuntimeServiceNode], contracts: List[DependencyContract]) -> List[RuntimeServiceEdge]:
    edges = []

    for contract in contracts:
        edge = RuntimeServiceEdge(
            edge_id=create_edge_id(),
            source_service_id=contract.source_service_id,
            target_service_id=contract.target_service_id,
            dependency_type=contract.dependency_type,
            required=contract.dependency_type == "REQUIRED",
            read_only=True,
            metadata_only=True,
            future_phase=False,
            blocked=False,
            rationale="Generated from dependency contract"
        )
        edges.append(edge)

    return edges

def build_dependency_adjacency(edges: List[RuntimeServiceEdge]) -> Dict[str, List[str]]:
    adj = {}
    for edge in edges:
        if edge.source_service_id not in adj:
            adj[edge.source_service_id] = []
        adj[edge.source_service_id].append(edge.target_service_id)
    return adj

def find_missing_dependencies(nodes: List[RuntimeServiceNode], edges: List[RuntimeServiceEdge]) -> List[str]:
    node_ids = {n.service_id for n in nodes}
    missing = []

    for edge in edges:
        if edge.target_service_id not in node_ids:
            missing.append(f"{edge.source_service_id} -> {edge.target_service_id} (missing target)")

    return missing

def dependency_graph_summary(nodes: List[RuntimeServiceNode], edges: List[RuntimeServiceEdge]) -> Dict[str, Any]:
    return {
        "node_count": len(nodes),
        "edge_count": len(edges)
    }

def dependency_graph_to_text(nodes: List[RuntimeServiceNode], edges: List[RuntimeServiceEdge], limit: int = 200) -> str:
    return f"Graph has {len(nodes)} nodes and {len(edges)} edges."
