from typing import Any, Dict, List, Tuple, Optional
from usa_signal_bot.runtime_service_graph.phase103_models import RuntimeServiceGraph
from usa_signal_bot.runtime_service_graph.dependency_graph import build_dependency_adjacency

def topological_sort_services(graph: RuntimeServiceGraph) -> Tuple[List[str], List[str]]:
    adj = build_dependency_adjacency(graph.edges)

    in_degree = {n.service_id: 0 for n in graph.nodes}
    for u in adj:
        for v in adj[u]:
            if v in in_degree:
                in_degree[v] += 1

    queue = [u for u in in_degree if in_degree[u] == 0]
    order = []

    while queue:
        u = queue.pop(0)
        order.append(u)
        for v in adj.get(u, []):
            if v in in_degree:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

    unresolved = [u for u in in_degree if in_degree[u] > 0]
    return order, unresolved

def plan_startup_order(graph: RuntimeServiceGraph) -> List[str]:
    if graph.graph_has_cycles:
        return []
    order, unresolved = topological_sort_services(graph)
    if unresolved:
        return []
    return order

def startup_order_summary(order: List[str], unresolved: Optional[List[str]] = None) -> Dict[str, Any]:
    return {
        "success": len(order) > 0 and not unresolved,
        "ordered_count": len(order),
        "unresolved_count": len(unresolved) if unresolved else 0
    }

def startup_order_to_text(order: List[str]) -> str:
    if not order:
        return "Failed to plan startup order."
    return f"Startup order planned with {len(order)} services."
