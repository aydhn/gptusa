from typing import Any, List
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_models import (
    ShadowLaunchReplayItem,
    ShadowLaunchReplayPlan,
    ShadowLaunchReplayResult,
    BoardEvidenceFreezeItem,
    BoardEvidenceFreezeBundle,
    DryAdmissionGateRule,
    DryAdmissionGateAssertion,
    FinalPaperModeDryAdmissionGate,
    DryAdmissionGateAuditEntry,
    DryAdmissionGateFullReview
)
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_report import dry_admission_gate_limitations_text

def shadow_launch_replay_item_to_text(item: ShadowLaunchReplayItem) -> str:
    return f"ShadowReplayItem({item.replay_item_id}): blocked={item.blocked}"

def shadow_launch_replay_plan_to_text(item: ShadowLaunchReplayPlan) -> str:
    return f"ShadowReplayPlan({item.replay_plan_id})"

def shadow_launch_replay_result_to_text(item: ShadowLaunchReplayResult) -> str:
    return f"ShadowReplayResult({item.replay_result_id}): passed={item.passed}, allowed={item.allowed_attempt_count}"

def board_evidence_freeze_item_to_text(item: BoardEvidenceFreezeItem) -> str:
    return f"BoardEvidenceFreezeItem({item.freeze_item_id}): available={item.available}"

def board_evidence_freeze_bundle_to_text(item: BoardEvidenceFreezeBundle, limit: int = 100) -> str:
    return f"BoardEvidenceFreezeBundle({item.freeze_id}): missing={item.missing_evidence_count}"

def dry_admission_gate_rule_to_text(item: DryAdmissionGateRule) -> str:
    return f"DryAdmissionGateRule({item.rule_id}): {item.rule_name}={item.status.value}"

def dry_admission_gate_assertion_to_text(item: DryAdmissionGateAssertion) -> str:
    return f"DryAdmissionGateAssertion({item.assertion_id}): {item.assertion_name}={item.status.value}"

def final_dry_admission_gate_to_text(item: FinalPaperModeDryAdmissionGate, limit: int = 100) -> str:
    return f"FinalPaperModeDryAdmissionGate({item.gate_id}): passed={item.dry_admission_gate_passed}"

def dry_admission_gate_audit_entry_to_text(item: DryAdmissionGateAuditEntry) -> str:
    return f"DryAdmissionGateAuditEntry({item.audit_id}): {item.action} on {item.entity_type}"

def dry_admission_gate_full_review_to_text(item: DryAdmissionGateFullReview, limit: int = 100) -> str:
    passed = item.gates[-1].dry_admission_gate_passed if item.gates else False
    return f"DryAdmissionGateFullReview({item.review_id}): passed={passed}\n{dry_admission_gate_limitations_text()}"

def dry_admission_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Store Summary: {summary}"
