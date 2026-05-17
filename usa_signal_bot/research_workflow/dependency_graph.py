from typing import Any, List, Dict
from .workflow_models import ExperimentPlan

def build_experiment_dependency_graph(plans: List[ExperimentPlan]) -> Dict[str, List[str]]:
    graph = {}
    for plan in plans:
        graph[plan.experiment_id] = list(plan.dependency_ids)
    return graph

def detect_dependency_cycles(graph: Dict[str, List[str]]) -> List[List[str]]:
    visited = set()
    path = []
    cycles = []

    def dfs(node):
        if node in path:
            cycle_idx = path.index(node)
            cycles.append(path[cycle_idx:] + [node])
            return
        if node in visited:
            return
        visited.add(node)
        path.append(node)
        for neighbor in graph.get(node, []):
            dfs(neighbor)
        path.pop()

    for node in graph:
        dfs(node)

    return cycles

def topological_experiment_order(plans: List[ExperimentPlan]) -> List[str]:
    graph = build_experiment_dependency_graph(plans)
    visited = set()
    order = []

    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        for neighbor in graph.get(node, []):
            dfs(neighbor)
        order.append(node)

    for plan in plans:
        dfs(plan.experiment_id)

    return order[::-1] # return reversed post-order

def dependency_graph_warnings(graph: Dict[str, List[str]]) -> List[str]:
    cycles = detect_dependency_cycles(graph)
    warnings = []
    for c in cycles:
        warnings.append(f"Dependency cycle detected: {' -> '.join(c)}")
    return warnings

def dependency_graph_to_text(graph: Dict[str, List[str]]) -> str:
    lines = ["Experiment Dependency Graph:"]
    for node, deps in graph.items():
        lines.append(f"  {node} -> {deps}")
    return "\n".join(lines)
