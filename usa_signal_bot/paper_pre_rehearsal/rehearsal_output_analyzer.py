from typing import Any, Dict, List
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_models import PrePaperDryRehearsalRun, MutationFirewallEvent

def count_firewall_events_by_type(events: List[MutationFirewallEvent]) -> Dict[str, int]:
    counts = {}
    for event in events:
        t = event.attempt_type.value
        counts[t] = counts.get(t, 0) + 1
    return counts

def count_firewall_events_by_action(events: List[MutationFirewallEvent]) -> Dict[str, int]:
    counts = {}
    for event in events:
        a = event.action.value
        counts[a] = counts.get(a, 0) + 1
    return counts

def count_blocked_firewall_events(events: List[MutationFirewallEvent]) -> int:
    return sum(1 for e in events if e.blocked)

def rehearsal_output_warning_flags(run: PrePaperDryRehearsalRun) -> List[str]:
    warnings = []
    if not run.plan:
        warnings.append("Missing plan")
    elif not run.plan.activation_denied_required:
        warnings.append("activation_denied_required is False")

    if len(run.firewall_rules) == 0:
        warnings.append("No firewall rules applied")

    blocked_count = count_blocked_firewall_events(run.firewall_events)
    if blocked_count < len(run.firewall_events):
        warnings.append("Not all firewall events were blocked")

    return warnings

def analyze_pre_paper_rehearsal_run(run: PrePaperDryRehearsalRun) -> Dict[str, Any]:
    events = run.firewall_events
    return {
        "firewall_rule_count": len(run.firewall_rules),
        "firewall_event_count": len(events),
        "blocked_event_count": count_blocked_firewall_events(events),
        "events_by_type": count_firewall_events_by_type(events),
        "events_by_action": count_firewall_events_by_action(events),
        "read_only_baseline_hash_present": bool(run.read_only_paper_baseline),
        "activation_denied_required": run.plan.activation_denied_required if run.plan else False,
        "safety_flag_count": len(run.safety_flags),
        "warnings": rehearsal_output_warning_flags(run)
    }

def rehearsal_output_analyzer_to_text(payload: Dict[str, Any]) -> str:
    return f"Analysis: {payload['firewall_event_count']} events ({payload['blocked_event_count']} blocked). Warnings: {len(payload['warnings'])}"
