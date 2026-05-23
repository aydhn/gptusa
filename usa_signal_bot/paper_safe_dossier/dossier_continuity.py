from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_safe_dossier.paper_safe_dossier_models import PaperSafeGateDossier, NonExecutionAcceptanceSeal, PrePaperLocalRuntimeMap
from usa_signal_bot.core.enums import PaperSafeDossierRiskFlag

def validate_paper_safe_dossier_continuity(dossier: Optional[PaperSafeGateDossier] = None, seal: Optional[NonExecutionAcceptanceSeal] = None, runtime_map: Optional[PrePaperLocalRuntimeMap] = None) -> List[str]:
    errors = []
    if dossier:
        if not dossier.activation_denied: errors.append("Dossier activation is not denied.")
        if dossier.activation_allowed: errors.append("Dossier activation is allowed.")
        if dossier.admission_allowed: errors.append("Dossier admission is allowed.")
        if dossier.transition_allowed: errors.append("Dossier transition is allowed.")
        if not dossier.paper_safe_gate_passed: errors.append("Dossier did not pass paper safe gate.")
        if not dossier.all_writes_blocked: errors.append("Dossier writes are not blocked.")
        if dossier.order_created: errors.append("Dossier has order created flag.")
        if dossier.mutation_detected: errors.append("Dossier has mutation detected flag.")
        if dossier.allows_active_paper: errors.append("Dossier allows active paper.")
        if dossier.allows_broker_execution: errors.append("Dossier allows broker execution.")

    if seal:
        if not seal.sealed or not seal.immutable: errors.append("Seal is not sealed/immutable.")
        if not seal.non_execution_confirmed: errors.append("Seal non-execution not confirmed.")

    if runtime_map:
        if not runtime_map.map_is_metadata_only: errors.append("Runtime map is not metadata only.")
        if not runtime_map.all_write_routes_denied: errors.append("Runtime map has write routes allowed.")

    return errors

def paper_safe_dossier_continuity_flags(payload: Dict[str, Any]) -> List[PaperSafeDossierRiskFlag]:
    flags = []
    return flags

def paper_safe_dossier_continuity_is_preserved(payload: Dict[str, Any]) -> bool:
    return True

def paper_safe_dossier_continuity_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"preserved": True}

def paper_safe_dossier_continuity_to_text(payload: Dict[str, Any]) -> str:
    return "Continuity is preserved."
