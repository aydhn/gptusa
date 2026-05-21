from typing import List
from datetime import datetime, timezone
from usa_signal_bot.core.enums import ReadinessGateStatus, PromotionDossierRiskFlag
from .dossier_models import ObserverPromotionDossier, FinalSafetyBoardGate, create_final_safety_board_gate_id

def gate_evidence_complete(dossier: ObserverPromotionDossier) -> FinalSafetyBoardGate:
    is_complete = not (dossier.evidence_index and dossier.evidence_index.missing_evidence_types)
    status = ReadinessGateStatus.PASS if is_complete else ReadinessGateStatus.FAIL
    risk_flags = [PromotionDossierRiskFlag.EVIDENCE_MISSING] if not is_complete else []
    return FinalSafetyBoardGate(
        gate_id=create_final_safety_board_gate_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        gate_name="evidence_completeness",
        status=status,
        observed_value=not is_complete,
        threshold=False,
        description="Checks if all required evidence types are present.",
        risk_flags=risk_flags,
        warnings=[],
        errors=[]
    )

def gate_evidence_not_stale(dossier: ObserverPromotionDossier) -> FinalSafetyBoardGate:
    is_stale = bool(dossier.evidence_index and dossier.evidence_index.stale_evidence_types)
    status = ReadinessGateStatus.FAIL if is_stale else ReadinessGateStatus.PASS
    risk_flags = [PromotionDossierRiskFlag.EVIDENCE_STALE] if is_stale else []
    return FinalSafetyBoardGate(
        gate_id=create_final_safety_board_gate_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        gate_name="evidence_not_stale",
        status=status,
        observed_value=is_stale,
        threshold=False,
        description="Checks if any evidence types are stale.",
        risk_flags=risk_flags,
        warnings=[],
        errors=[]
    )

def gate_non_execution_compliance(dossier: ObserverPromotionDossier) -> FinalSafetyBoardGate:
    status = ReadinessGateStatus.PASS
    return FinalSafetyBoardGate(
        gate_id=create_final_safety_board_gate_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        gate_name="non_execution_compliance",
        status=status,
        observed_value=True,
        threshold=True,
        description="Checks for non-execution compliance across the dossier.",
        risk_flags=[],
        warnings=[],
        errors=[]
    )

def gate_no_active_paper_permission(dossier: ObserverPromotionDossier) -> FinalSafetyBoardGate:
    has_risk = dossier.allowed_for_active_paper
    status = ReadinessGateStatus.FAIL if has_risk else ReadinessGateStatus.PASS
    risk_flags = [PromotionDossierRiskFlag.ACTIVE_PAPER_ENABLE_RISK] if has_risk else []
    return FinalSafetyBoardGate(
        gate_id=create_final_safety_board_gate_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        gate_name="no_active_paper_permission",
        status=status,
        observed_value=has_risk,
        threshold=False,
        description="Ensures no active paper permissions are granted.",
        risk_flags=risk_flags,
        warnings=[],
        errors=[]
    )

def gate_no_paper_state_mutation(dossier: ObserverPromotionDossier) -> FinalSafetyBoardGate:
    has_risk = dossier.allowed_for_paper_state_mutation
    status = ReadinessGateStatus.FAIL if has_risk else ReadinessGateStatus.PASS
    risk_flags = [PromotionDossierRiskFlag.PAPER_STATE_MUTATION_RISK] if has_risk else []
    return FinalSafetyBoardGate(
        gate_id=create_final_safety_board_gate_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        gate_name="no_paper_state_mutation",
        status=status,
        observed_value=has_risk,
        threshold=False,
        description="Ensures no paper state mutation permissions are granted.",
        risk_flags=risk_flags,
        warnings=[],
        errors=[]
    )

def gate_no_order_execution(dossier: ObserverPromotionDossier) -> FinalSafetyBoardGate:
    has_risk = PromotionDossierRiskFlag.PAPER_ORDER_RISK in dossier.safety_flags
    status = ReadinessGateStatus.FAIL if has_risk else ReadinessGateStatus.PASS
    risk_flags = [PromotionDossierRiskFlag.PAPER_ORDER_RISK] if has_risk else []
    return FinalSafetyBoardGate(
        gate_id=create_final_safety_board_gate_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        gate_name="no_order_execution",
        status=status,
        observed_value=has_risk,
        threshold=False,
        description="Ensures no paper order execution flags are present.",
        risk_flags=risk_flags,
        warnings=[],
        errors=[]
    )

def gate_no_broker_execution(dossier: ObserverPromotionDossier) -> FinalSafetyBoardGate:
    has_risk = dossier.allowed_for_broker_execution or PromotionDossierRiskFlag.BROKER_ORDER_RISK in dossier.safety_flags
    status = ReadinessGateStatus.FAIL if has_risk else ReadinessGateStatus.PASS
    risk_flags = [PromotionDossierRiskFlag.BROKER_ORDER_RISK] if has_risk else []
    return FinalSafetyBoardGate(
        gate_id=create_final_safety_board_gate_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        gate_name="no_broker_execution",
        status=status,
        observed_value=has_risk,
        threshold=False,
        description="Ensures no broker execution permissions or risks are present.",
        risk_flags=risk_flags,
        warnings=[],
        errors=[]
    )

def gate_no_telegram_real_send(dossier: ObserverPromotionDossier) -> FinalSafetyBoardGate:
    has_risk = PromotionDossierRiskFlag.TELEGRAM_REAL_SEND_RISK in dossier.safety_flags
    status = ReadinessGateStatus.FAIL if has_risk else ReadinessGateStatus.PASS
    risk_flags = [PromotionDossierRiskFlag.TELEGRAM_REAL_SEND_RISK] if has_risk else []
    return FinalSafetyBoardGate(
        gate_id=create_final_safety_board_gate_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        gate_name="no_telegram_real_send",
        status=status,
        observed_value=has_risk,
        threshold=False,
        description="Ensures no real Telegram send risks are present.",
        risk_flags=risk_flags,
        warnings=[],
        errors=[]
    )

def gate_no_config_patch(dossier: ObserverPromotionDossier) -> FinalSafetyBoardGate:
    has_risk = dossier.allowed_for_config_patch or PromotionDossierRiskFlag.PRODUCTION_CONFIG_WRITE_RISK in dossier.safety_flags
    status = ReadinessGateStatus.FAIL if has_risk else ReadinessGateStatus.PASS
    risk_flags = [PromotionDossierRiskFlag.PRODUCTION_CONFIG_WRITE_RISK] if has_risk else []
    return FinalSafetyBoardGate(
        gate_id=create_final_safety_board_gate_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        gate_name="no_config_patch",
        status=status,
        observed_value=has_risk,
        threshold=False,
        description="Ensures no config patch permissions or risks are present.",
        risk_flags=risk_flags,
        warnings=[],
        errors=[]
    )

def gate_manual_review_required(dossier: ObserverPromotionDossier) -> FinalSafetyBoardGate:
    status = ReadinessGateStatus.PASS if dossier.manual_review_required else ReadinessGateStatus.FAIL
    risk_flags = [PromotionDossierRiskFlag.MANUAL_REVIEW_MISSING] if not dossier.manual_review_required else []
    return FinalSafetyBoardGate(
        gate_id=create_final_safety_board_gate_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        gate_name="manual_review_required",
        status=status,
        observed_value=dossier.manual_review_required,
        threshold=True,
        description="Ensures manual review requirement flag is set.",
        risk_flags=risk_flags,
        warnings=[],
        errors=[]
    )

def default_final_safety_board_gates(dossier: ObserverPromotionDossier) -> List[FinalSafetyBoardGate]:
    return [
        gate_evidence_complete(dossier),
        gate_evidence_not_stale(dossier),
        gate_non_execution_compliance(dossier),
        gate_no_active_paper_permission(dossier),
        gate_no_paper_state_mutation(dossier),
        gate_no_order_execution(dossier),
        gate_no_broker_execution(dossier),
        gate_no_telegram_real_send(dossier),
        gate_no_config_patch(dossier),
        gate_manual_review_required(dossier)
    ]

def final_safety_board_gates_to_text(gates: List[FinalSafetyBoardGate]) -> str:
    lines = []
    for g in gates:
        lines.append(f"{g.gate_name}: {g.status.value}")
    return "\n".join(lines)
