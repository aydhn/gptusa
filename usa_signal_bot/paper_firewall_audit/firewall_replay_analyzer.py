from typing import Any, List
from usa_signal_bot.paper_firewall_audit.firewall_audit_models import FirewallReplayResult
from usa_signal_bot.core.enums import FirewallReplayOutcome

def analyze_firewall_replay_result(result: FirewallReplayResult) -> dict[str, Any]:
    return {
        "passed": result.passed,
        "followups": replay_followups(result)
    }

def replay_passed_all_required_attempts(result: FirewallReplayResult) -> bool:
    return result.outcome == FirewallReplayOutcome.ALL_DANGEROUS_ATTEMPTS_BLOCKED

def replay_requires_followup(result: FirewallReplayResult) -> bool:
    return not result.passed

def replay_followups(result: FirewallReplayResult) -> List[str]:
    f = []
    if not result.passed:
        f.append("Fix firewall rules to block all dangerous attempts")
    return f

def replay_result_risk_summary(result: FirewallReplayResult) -> dict[str, Any]:
    return {
        "unblocked": result.unblocked_dangerous_event_count,
        "flags": [f.value if hasattr(f, "value") else f for f in result.risk_flags]
    }

def firewall_replay_analyzer_to_text(payload: dict[str, Any]) -> str:
    return f"Analyzer passed: {payload.get('passed')}"
