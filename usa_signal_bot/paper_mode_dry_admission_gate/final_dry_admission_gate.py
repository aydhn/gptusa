import hashlib
import json
from datetime import datetime, timezone
from typing import Any, List
from usa_signal_bot.core.enums import PaperModeDryAdmissionGateStatus, PaperModeDryAdmissionGateDecision, DryAdmissionGateRiskFlag, DryAdmissionGateRuleStatus, DryAdmissionGateAssertionStatus
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_models import (
    FinalPaperModeDryAdmissionGate,
    DryAdmissionGateRule,
    DryAdmissionGateAssertion,
    ShadowLaunchReplayResult,
    BoardEvidenceFreezeBundle,
    create_final_dry_admission_gate_id
)
from usa_signal_bot.paper_mode_dry_admission_gate.board_dossier_ingestion import extract_board_dossier_candidate_id, extract_board_dossier, extract_acceptance_board_seal

def stable_dry_admission_gate_hash(payload: dict[str, Any]) -> str:
    s = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def collect_dry_admission_gate_safety_flags(board_payload: dict[str, Any], rules: List[DryAdmissionGateRule], assertions: List[DryAdmissionGateAssertion]) -> List[DryAdmissionGateRiskFlag]:
    flags = []
    for r in rules:
        flags.extend(r.risk_flags)
    for a in assertions:
        flags.extend(a.risk_flags)
    return list(set(flags))

def build_final_paper_mode_dry_admission_gate(board_payload: dict[str, Any]) -> FinalPaperModeDryAdmissionGate:
    candidate_id = extract_board_dossier_candidate_id(board_payload)
    dossier = extract_board_dossier(board_payload)
    seal = extract_acceptance_board_seal(board_payload)

    rules = board_payload.get("rules", []) # Passed in
    assertions = board_payload.get("assertions", []) # Passed in

    flags = collect_dry_admission_gate_safety_flags(board_payload, rules, assertions)
    passed = len(flags) == 0

    status = PaperModeDryAdmissionGateStatus.VALIDATED_DRY_ADMISSION_SAFE if passed else PaperModeDryAdmissionGateStatus.BLOCKED
    decision = PaperModeDryAdmissionGateDecision.PASS_TO_DRY_ADMISSION_GATE_DOSSIER if passed else PaperModeDryAdmissionGateDecision.BLOCK

    payload_for_hash = {"candidate_id": candidate_id, "dossier_id": dossier.get("dossier_id") if dossier else None}

    return FinalPaperModeDryAdmissionGate(
        gate_id=create_final_dry_admission_gate_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=status,
        decision=decision,
        rules=rules,
        assertions=assertions,
        sealed=True,
        immutable=True,
        manual_review_required=True,
        activation_denied=True,
        activation_allowed=False,
        admission_allowed=False,
        transition_allowed=False,
        shadow_launch_allowed=False,
        paper_mode_launch_allowed=False,
        dry_admission_gate_passed=passed,
        board_dossier_valid=dossier is not None,
        acceptance_seal_valid=seal is not None,
        all_writes_blocked=True,
        order_created=False,
        mutation_detected=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        safety_flags=flags,
        required_followups=["Resolve safety flags"] if not passed else [],
        warnings=[],
        errors=[],
        candidate_id=candidate_id,
        source_board_dossier_id=dossier.get("dossier_id") if dossier else None,
        source_acceptance_seal_id=seal.get("seal_id") if seal else None,
        gate_hash=stable_dry_admission_gate_hash(payload_for_hash)
    )

def build_default_final_dry_admission_gate(candidate_id: str | None = None) -> FinalPaperModeDryAdmissionGate:
    payload_for_hash = {"candidate_id": candidate_id}
    return FinalPaperModeDryAdmissionGate(
        gate_id=create_final_dry_admission_gate_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=PaperModeDryAdmissionGateStatus.DRAFT,
        decision=PaperModeDryAdmissionGateDecision.UNKNOWN,
        rules=[],
        assertions=[],
        sealed=True,
        immutable=True,
        manual_review_required=True,
        activation_denied=True,
        activation_allowed=False,
        admission_allowed=False,
        transition_allowed=False,
        shadow_launch_allowed=False,
        paper_mode_launch_allowed=False,
        dry_admission_gate_passed=False,
        board_dossier_valid=False,
        acceptance_seal_valid=False,
        all_writes_blocked=True,
        order_created=False,
        mutation_detected=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        safety_flags=[],
        required_followups=[],
        warnings=[],
        errors=[],
        candidate_id=candidate_id,
        gate_hash=stable_dry_admission_gate_hash(payload_for_hash)
    )

def final_dry_admission_gate_summary(gate: FinalPaperModeDryAdmissionGate) -> dict[str, Any]:
    return {
        "gate_id": gate.gate_id,
        "status": gate.status.value,
        "decision": gate.decision.value,
        "passed": gate.dry_admission_gate_passed,
        "flags_count": len(gate.safety_flags)
    }

def final_dry_admission_gate_to_text(gate: FinalPaperModeDryAdmissionGate, limit: int = 100) -> str:
    summary = final_dry_admission_gate_summary(gate)
    return f"Final Dry Admission Gate {summary['gate_id']} - Passed: {summary['passed']}"
