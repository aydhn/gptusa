from typing import Any, List
from usa_signal_bot.paper_firewall_audit.firewall_audit_models import ZeroMutationBaseline
from usa_signal_bot.core.enums import FirewallAuditRiskFlag

def compare_baseline_hashes(before: ZeroMutationBaseline, after: ZeroMutationBaseline) -> dict[str, Any]:
    changed = before.paper_snapshot_hash != after.paper_snapshot_hash
    return {
        "changed": changed,
        "before_hash": before.paper_snapshot_hash,
        "after_hash": after.paper_snapshot_hash
    }

def baseline_hash_changed(before: ZeroMutationBaseline, after: ZeroMutationBaseline) -> bool:
    return before.paper_snapshot_hash != after.paper_snapshot_hash

def baseline_hash_comparison_risk_flags(payload: dict[str, Any]) -> List[FirewallAuditRiskFlag]:
    if payload.get("changed", False):
        return [FirewallAuditRiskFlag.BASELINE_HASH_CHANGED]
    return []

def baseline_hash_comparison_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"changed": payload.get("changed", False)}

def baseline_hash_comparison_to_text(payload: dict[str, Any]) -> str:
    return f"Hash changed: {payload.get('changed', False)}"
