
from typing import Any, Dict, List
from usa_signal_bot.paper_safe_gate.paper_safe_gate_models import BoundaryCertificateReplayResult

def analyze_boundary_replay_result(result: BoundaryCertificateReplayResult) -> Dict[str, Any]:
    return {"passed": result.passed}

def boundary_replay_passed(result: BoundaryCertificateReplayResult) -> bool:
    return result.passed

def boundary_replay_requires_followup(result: BoundaryCertificateReplayResult) -> bool:
    return not result.passed

def boundary_replay_followups(result: BoundaryCertificateReplayResult) -> List[str]:
    return []

def boundary_replay_risk_summary(result: BoundaryCertificateReplayResult) -> Dict[str, Any]:
    return {"risk_flags": result.risk_flags}

def boundary_replay_analyzer_to_text(payload: Dict[str, Any]) -> str:
    return "Boundary Replay Analyzer: Clear"
