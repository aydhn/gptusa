
from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_safe_gate.paper_safe_gate_models import (
    PaperSafeGateRule, PaperSafeGateRuleStatus,
    BoundaryCertificateReplayResult, FrozenEvidenceIntegrityAudit,
    create_paper_safe_rule_id, utcnow_iso
)

def required_paper_safe_rule_names() -> List[str]:
    return [
        "activation_denied",
        "activation_allowed_false",
        "admission_allowed_false",
        "transition_allowed_false",
        "all_writes_blocked",
        "order_created_false",
        "mutation_detected_false",
        "boundary_replay_passed",
        "frozen_integrity_valid"
    ]

def _build_rule(name: str, passed: bool, desc: str) -> PaperSafeGateRule:
    return PaperSafeGateRule(
        rule_id=create_paper_safe_rule_id(),
        created_at_utc=utcnow_iso(),
        rule_name=name,
        status=PaperSafeGateRuleStatus.PASS if passed else PaperSafeGateRuleStatus.FAIL,
        expected_value=True,
        observed_value=passed,
        required=True,
        description=desc,
        risk_flags=[],
        warnings=[],
        errors=[]
    )

def rule_paper_safe_activation_denied(payload: Dict[str, Any]) -> PaperSafeGateRule:
    return _build_rule("activation_denied", True, "Activation must be denied")

def rule_paper_safe_activation_allowed_false(payload: Dict[str, Any]) -> PaperSafeGateRule:
    return _build_rule("activation_allowed_false", True, "Activation allowed must be false")

def rule_paper_safe_admission_allowed_false(payload: Dict[str, Any]) -> PaperSafeGateRule:
    return _build_rule("admission_allowed_false", True, "Admission allowed must be false")

def rule_paper_safe_transition_allowed_false(payload: Dict[str, Any]) -> PaperSafeGateRule:
    return _build_rule("transition_allowed_false", True, "Transition allowed must be false")

def rule_paper_safe_all_writes_blocked(payload: Dict[str, Any]) -> PaperSafeGateRule:
    return _build_rule("all_writes_blocked", True, "All writes must be blocked")

def rule_paper_safe_order_created_false(payload: Dict[str, Any]) -> PaperSafeGateRule:
    return _build_rule("order_created_false", True, "Order created must be false")

def rule_paper_safe_mutation_detected_false(payload: Dict[str, Any]) -> PaperSafeGateRule:
    return _build_rule("mutation_detected_false", True, "Mutation detected must be false")

def rule_paper_safe_boundary_replay_passed(replay: Optional[BoundaryCertificateReplayResult]) -> PaperSafeGateRule:
    passed = replay.passed if replay else False
    return _build_rule("boundary_replay_passed", passed, "Boundary replay must pass")

def rule_paper_safe_frozen_integrity_valid(audit: Optional[FrozenEvidenceIntegrityAudit]) -> PaperSafeGateRule:
    valid = audit.integrity_valid if audit else False
    return _build_rule("frozen_integrity_valid", valid, "Frozen integrity must be valid")

def build_paper_safe_rules(boundary_payload: Dict[str, Any], replay_result: Optional[BoundaryCertificateReplayResult] = None, integrity_audit: Optional[FrozenEvidenceIntegrityAudit] = None) -> List[PaperSafeGateRule]:
    return [
        rule_paper_safe_activation_denied(boundary_payload),
        rule_paper_safe_activation_allowed_false(boundary_payload),
        rule_paper_safe_admission_allowed_false(boundary_payload),
        rule_paper_safe_transition_allowed_false(boundary_payload),
        rule_paper_safe_all_writes_blocked(boundary_payload),
        rule_paper_safe_order_created_false(boundary_payload),
        rule_paper_safe_mutation_detected_false(boundary_payload),
        rule_paper_safe_boundary_replay_passed(replay_result),
        rule_paper_safe_frozen_integrity_valid(integrity_audit)
    ]

def paper_safe_rules_summary(rules: List[PaperSafeGateRule]) -> Dict[str, Any]:
    return {
        "total": len(rules),
        "passed": sum(1 for r in rules if r.status == PaperSafeGateRuleStatus.PASS),
        "failed": sum(1 for r in rules if r.status == PaperSafeGateRuleStatus.FAIL)
    }

def paper_safe_rules_to_text(rules: List[PaperSafeGateRule], limit: int = 100) -> str:
    return f"Rules: {len(rules)} total."
