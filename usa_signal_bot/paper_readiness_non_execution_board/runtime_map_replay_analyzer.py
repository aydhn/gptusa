from typing import Any, Dict, List
from usa_signal_bot.paper_readiness_non_execution_board.non_execution_board_models import RuntimeMapReplayResult, RuntimeMapReplayOutcome

def analyze_runtime_map_replay_result(result: RuntimeMapReplayResult) -> Dict[str, Any]:
    return {
        "passed": result.passed,
        "requires_followup": runtime_map_replay_requires_followup(result),
        "followups": runtime_map_replay_followups(result),
        "risk_summary": runtime_map_replay_risk_summary(result)
    }

def runtime_map_replay_passed(result: RuntimeMapReplayResult) -> bool:
    return result.passed

def runtime_map_replay_requires_followup(result: RuntimeMapReplayResult) -> bool:
    return not result.passed or len(result.errors) > 0 or len(result.warnings) > 0

def runtime_map_replay_followups(result: RuntimeMapReplayResult) -> List[str]:
    followups = []
    if result.missing_component_count > 0:
        followups.append("Review missing components in component map")
    if result.missing_route_count > 0:
        followups.append("Review missing routes in route map")
    if result.dangerous_allowed_count > 0:
        followups.append("IMMEDIATE ACTION: Block dangerous allowed routes")
    return followups

def runtime_map_replay_risk_summary(result: RuntimeMapReplayResult) -> Dict[str, Any]:
    return {
        "flags": [f.value for f in result.risk_flags],
        "dangerous_allowed": result.dangerous_allowed_count > 0
    }

def runtime_map_replay_analyzer_to_text(payload: Dict[str, Any]) -> str:
    lines = ["--- RUNTIME MAP REPLAY ANALYZER ---"]
    lines.append(f"Passed: {payload.get('passed')}")
    lines.append(f"Requires Followup: {payload.get('requires_followup')}")
    if payload.get("followups"):
        lines.append("Followups:")
        for f in payload.get("followups"):
            lines.append(f"  - {f}")
    return "\n".join(lines)
