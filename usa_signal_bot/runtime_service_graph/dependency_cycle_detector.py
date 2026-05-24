from typing import Any, Dict, List
from usa_signal_bot.runtime_service_graph.phase103_models import RuntimeServiceEdge
from usa_signal_bot.runtime_service_graph.dependency_graph import build_dependency_adjacency

def detect_dependency_cycles(edges: List[RuntimeServiceEdge]) -> List[List[str]]:
    adj = build_dependency_adjacency(edges)

    visited = set()
    rec_stack = set()
    cycles = []

    def dfs(node: str, path: List[str]):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path)
            elif neighbor in rec_stack:
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:].copy() + [neighbor])

        rec_stack.remove(node)
        path.pop()

    for node in list(adj.keys()):
        if node not in visited:
            dfs(node, [])

    return cycles

def dependency_graph_has_cycles(edges: List[RuntimeServiceEdge]) -> bool:
    return len(detect_dependency_cycles(edges)) > 0

def cycle_detector_summary(edges: List[RuntimeServiceEdge]) -> Dict[str, Any]:
    cycles = detect_dependency_cycles(edges)
    return {
        "has_cycles": len(cycles) > 0,
        "cycle_count": len(cycles)
    }

def cycle_detector_to_text(cycles: List[List[str]]) -> str:
    if not cycles:
        return "No cycles detected."
    return f"Detected {len(cycles)} cycle(s)."
