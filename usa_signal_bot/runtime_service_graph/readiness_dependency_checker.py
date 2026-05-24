from typing import Any, Dict, List
from usa_signal_bot.runtime_service_graph.phase103_models import RuntimeServiceGraph

def services_ready_for_phase103(graph: RuntimeServiceGraph) -> List[str]:
    ready = []
    for node in graph.nodes:
        if node.status in ["READY_METADATA_ONLY", "READY_LOCAL_COMPUTE", "READY_READ_ONLY"]:
            ready.append(node.service_id)
    return ready

def services_blocked_for_phase103(graph: RuntimeServiceGraph) -> List[str]:
    blocked = []
    for node in graph.nodes:
        if node.status in ["BLOCKED", "FAILED"]:
            blocked.append(node.service_id)
    return blocked

def check_service_readiness_dependencies(graph: RuntimeServiceGraph) -> Dict[str, Any]:
    ready = services_ready_for_phase103(graph)
    blocked = services_blocked_for_phase103(graph)

    return {
        "ready_count": len(ready),
        "blocked_count": len(blocked),
        "total": len(graph.nodes)
    }

def readiness_dependency_checker_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload

def readiness_dependency_checker_to_text(payload: Dict[str, Any]) -> str:
    return f"Readiness: {payload.get('ready_count', 0)} ready, {payload.get('blocked_count', 0)} blocked out of {payload.get('total', 0)}."
