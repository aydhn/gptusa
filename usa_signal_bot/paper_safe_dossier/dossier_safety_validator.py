from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_safe_dossier.paper_safe_dossier_models import PaperSafeGateDossier, NonExecutionAcceptanceSeal, PrePaperLocalRuntimeMap
from usa_signal_bot.core.enums import PaperSafeDossierRiskFlag

def collect_paper_safe_dossier_safety_flags(dossier: Optional[PaperSafeGateDossier] = None, seal: Optional[NonExecutionAcceptanceSeal] = None, runtime_map: Optional[PrePaperLocalRuntimeMap] = None) -> List[PaperSafeDossierRiskFlag]:
    flags = []
    if dossier:
        flags.extend(dossier.safety_flags)
        if dossier.activation_allowed: flags.append(PaperSafeDossierRiskFlag.ACTIVATION_ALLOWED_RISK)
        if dossier.admission_allowed: flags.append(PaperSafeDossierRiskFlag.ADMISSION_ALLOWED_RISK)
        if dossier.order_created: flags.append(PaperSafeDossierRiskFlag.ORDER_CREATED_RISK)
        if dossier.mutation_detected: flags.append(PaperSafeDossierRiskFlag.MUTATION_DETECTED_RISK)

    if seal:
        flags.extend(seal.risk_flags)
        if not seal.non_execution_confirmed: flags.append(PaperSafeDossierRiskFlag.NON_EXECUTION_SEAL_FAILED)

    if runtime_map:
        flags.extend(runtime_map.risk_flags)
        if not runtime_map.map_is_metadata_only: flags.append(PaperSafeDossierRiskFlag.RUNTIME_MAP_INVALID)

    return list(set(flags))

def paper_safe_dossier_has_blocking_flags(flags: List[PaperSafeDossierRiskFlag]) -> bool:
    blocking = [
        PaperSafeDossierRiskFlag.REAL_ORDER_RISK,
        PaperSafeDossierRiskFlag.PAPER_ORDER_RISK,
        PaperSafeDossierRiskFlag.BROKER_ORDER_RISK,
        PaperSafeDossierRiskFlag.PAPER_STATE_MUTATION_RISK,
        PaperSafeDossierRiskFlag.TELEGRAM_REAL_SEND_RISK,
        PaperSafeDossierRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
        PaperSafeDossierRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
        PaperSafeDossierRiskFlag.ACTIVATION_ALLOWED_RISK,
        PaperSafeDossierRiskFlag.ADMISSION_ALLOWED_RISK,
        PaperSafeDossierRiskFlag.TRANSITION_ALLOWED_RISK,
        PaperSafeDossierRiskFlag.ORDER_CREATED_RISK,
        PaperSafeDossierRiskFlag.MUTATION_DETECTED_RISK,
        PaperSafeDossierRiskFlag.FROZEN_EVIDENCE_TAMPER_RISK,
        PaperSafeDossierRiskFlag.NON_EXECUTION_SEAL_FAILED,
        PaperSafeDossierRiskFlag.RUNTIME_MAP_INVALID,
        PaperSafeDossierRiskFlag.RUNTIME_ROUTE_PERMISSION_RISK,
        PaperSafeDossierRiskFlag.SECRET_RISK
    ]
    for flag in flags:
        if flag in blocking:
            return True
    return False

def validate_paper_safe_dossier_safety(dossier: Optional[PaperSafeGateDossier] = None, seal: Optional[NonExecutionAcceptanceSeal] = None, runtime_map: Optional[PrePaperLocalRuntimeMap] = None) -> List[str]:
    errors = []
    flags = collect_paper_safe_dossier_safety_flags(dossier, seal, runtime_map)
    if paper_safe_dossier_has_blocking_flags(flags):
         errors.append("Dossier has blocking safety flags.")
    return errors

def paper_safe_dossier_safety_summary(flags: List[PaperSafeDossierRiskFlag]) -> Dict[str, Any]:
    return {
        "is_safe": not paper_safe_dossier_has_blocking_flags(flags),
        "flag_count": len(flags),
        "flags": [f.value for f in flags]
    }

def paper_safe_dossier_safety_validator_to_text(payload: Dict[str, Any]) -> str:
    lines = [f"Is Safe: {payload.get('is_safe', False)}"]
    if payload.get("flag_count", 0) > 0:
        lines.append(f"Flags: {', '.join(payload.get('flags', []))}")
    return "\n".join(lines)
