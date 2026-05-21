from typing import Any, Dict, List
from usa_signal_bot.core.enums import PromotionDossierRiskFlag
from .dossier_models import ObserverPromotionDossier, FinalSafetyBoardReview, StagedPaperReadinessPackage

def validate_dossier_non_execution(dossier: ObserverPromotionDossier) -> Dict[str, Any]:
    flags = []
    if dossier.allowed_for_active_paper: flags.append(PromotionDossierRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
    if dossier.allowed_for_broker_execution: flags.append(PromotionDossierRiskFlag.BROKER_ORDER_RISK)
    if dossier.allowed_for_paper_state_mutation: flags.append(PromotionDossierRiskFlag.PAPER_STATE_MUTATION_RISK)
    if dossier.allowed_for_config_patch: flags.append(PromotionDossierRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)

    return {
        "valid": len(flags) == 0,
        "risk_flags": flags
    }

def validate_board_non_execution(board: FinalSafetyBoardReview) -> Dict[str, Any]:
    flags = []
    if board.allowed_for_active_paper: flags.append(PromotionDossierRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
    if board.allowed_for_broker_execution: flags.append(PromotionDossierRiskFlag.BROKER_ORDER_RISK)
    if board.allowed_for_paper_state_mutation: flags.append(PromotionDossierRiskFlag.PAPER_STATE_MUTATION_RISK)
    if board.allowed_for_config_patch: flags.append(PromotionDossierRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)

    return {
        "valid": len(flags) == 0,
        "risk_flags": flags
    }

def validate_package_non_execution(package: StagedPaperReadinessPackage) -> Dict[str, Any]:
    flags = []
    if package.allowed_for_active_paper: flags.append(PromotionDossierRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
    if package.allowed_for_broker_execution: flags.append(PromotionDossierRiskFlag.BROKER_ORDER_RISK)
    if package.allowed_for_paper_state_mutation: flags.append(PromotionDossierRiskFlag.PAPER_STATE_MUTATION_RISK)
    if package.allowed_for_config_patch: flags.append(PromotionDossierRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)

    for plan in package.stage_plans:
        if plan.execution_enabled: flags.append(PromotionDossierRiskFlag.REAL_ORDER_RISK)
        if plan.active_paper_enabled: flags.append(PromotionDossierRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
        if plan.broker_execution_enabled: flags.append(PromotionDossierRiskFlag.BROKER_ORDER_RISK)
        if plan.paper_state_mutation_enabled: flags.append(PromotionDossierRiskFlag.PAPER_STATE_MUTATION_RISK)
        if plan.config_patch_enabled: flags.append(PromotionDossierRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)

    return {
        "valid": len(flags) == 0,
        "risk_flags": list(set(flags))
    }

def collect_non_execution_risk_flags(payload: Dict[str, Any]) -> List[PromotionDossierRiskFlag]:
    return payload.get("risk_flags", [])

def non_execution_compliance_to_text(payload: Dict[str, Any]) -> str:
    valid = payload.get("valid", False)
    flags = payload.get("risk_flags", [])
    if valid:
        return "Non-execution compliance: PASSED."
    return f"Non-execution compliance: FAILED. Risks: {[f.value for f in flags]}"
