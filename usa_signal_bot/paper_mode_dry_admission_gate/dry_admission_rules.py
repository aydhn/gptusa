from datetime import datetime, timezone
from typing import Any, List
from usa_signal_bot.core.enums import DryAdmissionGateRuleStatus, DryAdmissionGateRiskFlag
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_models import (
    DryAdmissionGateRule,
    ShadowLaunchReplayResult,
    BoardEvidenceFreezeBundle,
    create_dry_admission_rule_id
)
from usa_signal_bot.paper_mode_dry_admission_gate.board_dossier_ingestion import extract_acceptance_board_seal

def required_dry_admission_rule_names() -> List[str]:
    return [
        "shadow_launch_allowed_false",
        "paper_mode_launch_allowed_false",
        "activation_allowed_false",
        "admission_allowed_false",
        "order_created_false",
        "mutation_detected_false",
        "acceptance_board_seal_valid",
        "shadow_replay_passed",
        "board_evidence_freeze_valid"
    ]

def build_dry_admission_rules(
    board_payload: dict[str, Any],
    replay_result: ShadowLaunchReplayResult | None = None,
    freeze_bundle: BoardEvidenceFreezeBundle | None = None
) -> List[DryAdmissionGateRule]:
    return [
        rule_shadow_launch_allowed_false(board_payload),
        rule_paper_mode_launch_allowed_false(board_payload),
        rule_activation_allowed_false(board_payload),
        rule_admission_allowed_false(board_payload),
        rule_order_created_false(board_payload),
        rule_mutation_detected_false(board_payload),
        rule_acceptance_board_seal_valid(board_payload),
        rule_shadow_replay_passed(replay_result),
        rule_board_evidence_freeze_valid(freeze_bundle)
    ]

def _create_rule(name: str, passed: bool, risk_flag: DryAdmissionGateRiskFlag | None, desc: str) -> DryAdmissionGateRule:
    status = DryAdmissionGateRuleStatus.PASS if passed else DryAdmissionGateRuleStatus.FAIL
    flags = [risk_flag] if not passed and risk_flag else []
    errors = ["Rule failed"] if not passed else []
    return DryAdmissionGateRule(
        rule_id=create_dry_admission_rule_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        rule_name=name,
        status=status,
        required=True,
        description=desc,
        risk_flags=flags,
        warnings=[],
        errors=errors
    )

def rule_shadow_launch_allowed_false(board_payload: dict[str, Any]) -> DryAdmissionGateRule:
    passed = not board_payload.get("shadow_launch_allowed", False)
    return _create_rule("shadow_launch_allowed_false", passed, DryAdmissionGateRiskFlag.SHADOW_LAUNCH_RISK, "Shadow launch must not be allowed")

def rule_paper_mode_launch_allowed_false(board_payload: dict[str, Any]) -> DryAdmissionGateRule:
    passed = not board_payload.get("paper_mode_launch_allowed", False)
    return _create_rule("paper_mode_launch_allowed_false", passed, DryAdmissionGateRiskFlag.PAPER_MODE_LAUNCH_RISK, "Paper mode launch must not be allowed")

def rule_activation_allowed_false(board_payload: dict[str, Any]) -> DryAdmissionGateRule:
    passed = not board_payload.get("activation_allowed", False)
    return _create_rule("activation_allowed_false", passed, DryAdmissionGateRiskFlag.ACTIVATION_ALLOWED_RISK, "Activation must not be allowed")

def rule_admission_allowed_false(board_payload: dict[str, Any]) -> DryAdmissionGateRule:
    passed = not board_payload.get("admission_allowed", False)
    return _create_rule("admission_allowed_false", passed, DryAdmissionGateRiskFlag.ADMISSION_ALLOWED_RISK, "Admission must not be allowed")

def rule_order_created_false(board_payload: dict[str, Any]) -> DryAdmissionGateRule:
    passed = not board_payload.get("order_created", False)
    return _create_rule("order_created_false", passed, DryAdmissionGateRiskFlag.ORDER_CREATED_RISK, "Order must not be created")

def rule_mutation_detected_false(board_payload: dict[str, Any]) -> DryAdmissionGateRule:
    passed = not board_payload.get("mutation_detected", False)
    return _create_rule("mutation_detected_false", passed, DryAdmissionGateRiskFlag.MUTATION_DETECTED_RISK, "Mutation must not be detected")

def rule_acceptance_board_seal_valid(board_payload: dict[str, Any]) -> DryAdmissionGateRule:
    seal = extract_acceptance_board_seal(board_payload)
    passed = seal is not None and seal.get("status") in ["VALIDATED", "SEALED"]
    return _create_rule("acceptance_board_seal_valid", passed, DryAdmissionGateRiskFlag.ACCEPTANCE_BOARD_SEAL_FAILED, "Acceptance board seal must be valid")

def rule_shadow_replay_passed(replay_result: ShadowLaunchReplayResult | None) -> DryAdmissionGateRule:
    passed = replay_result is not None and replay_result.passed
    return _create_rule("shadow_replay_passed", passed, DryAdmissionGateRiskFlag.SHADOW_REPLAY_FAILED, "Shadow replay must have passed")

def rule_board_evidence_freeze_valid(freeze_bundle: BoardEvidenceFreezeBundle | None) -> DryAdmissionGateRule:
    passed = freeze_bundle is not None and freeze_bundle.missing_evidence_count == 0
    return _create_rule("board_evidence_freeze_valid", passed, DryAdmissionGateRiskFlag.BOARD_EVIDENCE_FREEZE_FAILED, "Board evidence freeze must be valid")

def dry_admission_rules_summary(rules: List[DryAdmissionGateRule]) -> dict[str, Any]:
    passed = sum(1 for r in rules if r.status == DryAdmissionGateRuleStatus.PASS)
    failed = sum(1 for r in rules if r.status == DryAdmissionGateRuleStatus.FAIL)
    return {
        "total": len(rules),
        "passed": passed,
        "failed": failed,
        "all_passed": failed == 0
    }

def dry_admission_rules_to_text(rules: List[DryAdmissionGateRule], limit: int = 100) -> str:
    summary = dry_admission_rules_summary(rules)
    return f"Dry Admission Rules - Total: {summary['total']}, Passed: {summary['passed']}, Failed: {summary['failed']}"
