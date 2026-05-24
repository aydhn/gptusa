from typing import Any
from usa_signal_bot.core.enums import DryAdmissionDossierDecision, DryAdmissionDossierRiskFlag, DryAdmissionDossierStatus
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_gate_ingestion import dry_admission_gate_supports_dossier, extract_final_dry_admission_gate, extract_shadow_replay_result, extract_board_evidence_freeze

def dry_admission_dossier_safety_flags_from_payload(payload: dict[str, Any]) -> list[DryAdmissionDossierRiskFlag]:
    flags = []

    if payload.get("activation_allowed") is True:
        flags.append(DryAdmissionDossierRiskFlag.ACTIVATION_ALLOWED_RISK)
    if payload.get("admission_allowed") is True:
        flags.append(DryAdmissionDossierRiskFlag.ADMISSION_ALLOWED_RISK)
    if payload.get("transition_allowed") is True:
        flags.append(DryAdmissionDossierRiskFlag.TRANSITION_ALLOWED_RISK)
    if payload.get("shadow_launch_allowed") is True:
        flags.append(DryAdmissionDossierRiskFlag.SHADOW_LAUNCH_RISK)
    if payload.get("paper_mode_launch_allowed") is True:
        flags.append(DryAdmissionDossierRiskFlag.PAPER_MODE_LAUNCH_RISK)
    if payload.get("rehearsal_allowed") is True:
        flags.append(DryAdmissionDossierRiskFlag.PAPER_MODE_REHEARSAL_RISK)
    if payload.get("order_created") is True:
        flags.append(DryAdmissionDossierRiskFlag.ORDER_CREATED_RISK)
    if payload.get("mutation_detected") is True:
        flags.append(DryAdmissionDossierRiskFlag.MUTATION_DETECTED_RISK)

    gate = extract_final_dry_admission_gate(payload)
    if gate and gate.get("status") in ["FAILED", "MISSING"]:
        flags.append(DryAdmissionDossierRiskFlag.DRY_ADMISSION_GATE_FAILED)

    shadow_replay = extract_shadow_replay_result(payload)
    if shadow_replay and shadow_replay.get("status") in ["FAILED"]:
        flags.append(DryAdmissionDossierRiskFlag.SHADOW_REPLAY_FAILED)

    freeze = extract_board_evidence_freeze(payload)
    if freeze and freeze.get("status") in ["FAILED", "STALE"]:
        flags.append(DryAdmissionDossierRiskFlag.BOARD_EVIDENCE_FREEZE_FAILED)

    return list(set(flags))

def evaluate_dry_admission_dossier_eligibility(payload: dict[str, Any]) -> DryAdmissionDossierDecision:
    supports, _ = dry_admission_gate_supports_dossier(payload)
    flags = dry_admission_dossier_safety_flags_from_payload(payload)

    if DryAdmissionDossierRiskFlag.ACTIVATION_ALLOWED_RISK in flags or        DryAdmissionDossierRiskFlag.ADMISSION_ALLOWED_RISK in flags or        DryAdmissionDossierRiskFlag.TRANSITION_ALLOWED_RISK in flags or        DryAdmissionDossierRiskFlag.SHADOW_LAUNCH_RISK in flags or        DryAdmissionDossierRiskFlag.PAPER_MODE_LAUNCH_RISK in flags or        DryAdmissionDossierRiskFlag.ORDER_CREATED_RISK in flags or        DryAdmissionDossierRiskFlag.MUTATION_DETECTED_RISK in flags:
        return DryAdmissionDossierDecision.BLOCK

    gate = extract_final_dry_admission_gate(payload)
    if not gate or gate.get("status") in ["MISSING", "STALE"]:
        return DryAdmissionDossierDecision.REQUEST_DRY_ADMISSION_GATE_REFRESH

    if payload.get("decision") == "REQUEST_MANUAL_REVIEW":
        return DryAdmissionDossierDecision.REQUEST_MANUAL_REVIEW

    if payload.get("decision") == "REJECT":
        return DryAdmissionDossierDecision.REJECT

    if supports:
        return DryAdmissionDossierDecision.CREATE_DRY_ADMISSION_DOSSIER

    return DryAdmissionDossierDecision.INCONCLUSIVE

def dry_admission_dossier_eligibility_reasons(payload: dict[str, Any]) -> list[str]:
    _, reasons = dry_admission_gate_supports_dossier(payload)
    return reasons

def dry_admission_dossier_status_from_decision(decision: DryAdmissionDossierDecision) -> DryAdmissionDossierStatus:
    mapping = {
        DryAdmissionDossierDecision.CREATE_DRY_ADMISSION_DOSSIER: DryAdmissionDossierStatus.CREATED,
        DryAdmissionDossierDecision.REQUEST_DRY_ADMISSION_GATE_REFRESH: DryAdmissionDossierStatus.REQUEST_CHANGES,
        DryAdmissionDossierDecision.REQUEST_DRY_ADMISSION_ACCEPTANCE_SEAL_REFRESH: DryAdmissionDossierStatus.REQUEST_CHANGES,
        DryAdmissionDossierDecision.REQUEST_REHEARSAL_BLOCKER_REFRESH: DryAdmissionDossierStatus.REQUEST_CHANGES,
        DryAdmissionDossierDecision.REQUEST_MANUAL_REVIEW: DryAdmissionDossierStatus.REQUEST_CHANGES,
        DryAdmissionDossierDecision.REJECT: DryAdmissionDossierStatus.REJECTED,
        DryAdmissionDossierDecision.BLOCK: DryAdmissionDossierStatus.BLOCKED,
        DryAdmissionDossierDecision.INCONCLUSIVE: DryAdmissionDossierStatus.UNKNOWN,
        DryAdmissionDossierDecision.UNKNOWN: DryAdmissionDossierStatus.UNKNOWN,
    }
    return mapping.get(decision, DryAdmissionDossierStatus.UNKNOWN)

def eligibility_checker_to_text(payload: dict[str, Any]) -> str:
    decision = evaluate_dry_admission_dossier_eligibility(payload)
    reasons = dry_admission_dossier_eligibility_reasons(payload)

    text = f"Dry-Admission Dossier Eligibility:
"
    text += f"- Decision: {decision.value}
"
    if reasons:
        text += f"- Reasons: {', '.join(reasons)}
"
    return text
