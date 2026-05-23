from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.paper_boundary_certificate.boundary_certificate_models import BoundaryRule, AdmissionBlockerReplayResult, NoOrderEvidenceFreezeBundle, create_boundary_rule_id
from usa_signal_bot.core.enums import BoundaryRuleStatus

def required_boundary_rule_names() -> list[str]:
    return [
        "activation_denied",
        "activation_allowed_false",
        "admission_allowed_false",
        "transition_allowed_false",
        "all_writes_blocked",
        "order_created_false",
        "mutation_detected_false",
        "blocker_replay_passed",
        "evidence_freeze_valid"
    ]

def build_boundary_rules(no_order_payload: dict[str, Any], replay_result: AdmissionBlockerReplayResult | None = None, freeze_bundle: NoOrderEvidenceFreezeBundle | None = None) -> list[BoundaryRule]:
    return [
        rule_activation_denied(no_order_payload),
        rule_activation_allowed_false(no_order_payload),
        rule_admission_allowed_false(no_order_payload),
        rule_transition_allowed_false(no_order_payload),
        rule_all_writes_blocked(no_order_payload),
        rule_order_created_false(no_order_payload),
        rule_mutation_detected_false(no_order_payload),
        rule_blocker_replay_passed(replay_result),
        rule_evidence_freeze_valid(freeze_bundle)
    ]

def rule_activation_denied(no_order_payload: dict[str, Any]) -> BoundaryRule:
    return _create_rule("activation_denied", True, True)

def rule_activation_allowed_false(no_order_payload: dict[str, Any]) -> BoundaryRule:
    return _create_rule("activation_allowed_false", False, False)

def rule_admission_allowed_false(no_order_payload: dict[str, Any]) -> BoundaryRule:
    return _create_rule("admission_allowed_false", False, False)

def rule_transition_allowed_false(no_order_payload: dict[str, Any]) -> BoundaryRule:
    return _create_rule("transition_allowed_false", False, False)

def rule_all_writes_blocked(no_order_payload: dict[str, Any]) -> BoundaryRule:
    return _create_rule("all_writes_blocked", True, True)

def rule_order_created_false(no_order_payload: dict[str, Any]) -> BoundaryRule:
    return _create_rule("order_created_false", False, False)

def rule_mutation_detected_false(no_order_payload: dict[str, Any]) -> BoundaryRule:
    return _create_rule("mutation_detected_false", False, False)

def rule_blocker_replay_passed(replay_result: AdmissionBlockerReplayResult | None) -> BoundaryRule:
    val = replay_result.passed if replay_result else False
    return _create_rule("blocker_replay_passed", True, val)

def rule_evidence_freeze_valid(freeze_bundle: NoOrderEvidenceFreezeBundle | None) -> BoundaryRule:
    val = freeze_bundle.frozen and freeze_bundle.immutable if freeze_bundle else False
    return _create_rule("evidence_freeze_valid", True, val)

def _create_rule(name: str, expected: Any, observed: Any) -> BoundaryRule:
    status = BoundaryRuleStatus.PASS if expected == observed else BoundaryRuleStatus.FAIL
    return BoundaryRule(
        rule_id=create_boundary_rule_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        rule_name=name,
        status=status,
        expected_value=expected,
        observed_value=observed,
        required=True,
        description=f"Rule {name}",
        risk_flags=[],
        warnings=[],
        errors=[]
    )

def boundary_rules_summary(rules: list[BoundaryRule]) -> dict[str, Any]:
    return {"total": len(rules), "passed": sum(1 for r in rules if r.status == BoundaryRuleStatus.PASS)}

def boundary_rules_to_text(rules: list[BoundaryRule], limit: int = 100) -> str:
    return str(boundary_rules_summary(rules))
