from typing import Any, Dict, List
from usa_signal_bot.core.enums import PromotionDossierRiskFlag
from .dossier_models import StagedPaperReadinessPackage
from .readiness_stage_plan import validate_readiness_stage_plan_safety

def validate_package_no_activation(package: StagedPaperReadinessPackage) -> List[str]:
    warnings = []
    if package.allowed_for_active_paper: warnings.append("Package illegally enables active paper.")
    if package.allowed_for_broker_execution: warnings.append("Package illegally enables broker execution.")
    if package.allowed_for_paper_state_mutation: warnings.append("Package illegally enables paper state mutation.")
    if package.allowed_for_config_patch: warnings.append("Package illegally enables config patch.")
    return warnings

def validate_package_no_execution_flags(package: StagedPaperReadinessPackage) -> List[str]:
    warnings = []
    for plan in package.stage_plans:
        if plan.execution_enabled: warnings.append(f"Stage {plan.stage.value} illegally has execution_enabled=True.")
        if plan.active_paper_enabled: warnings.append(f"Stage {plan.stage.value} illegally has active_paper_enabled=True.")
        if plan.broker_execution_enabled: warnings.append(f"Stage {plan.stage.value} illegally has broker_execution_enabled=True.")
    return warnings

def validate_package_stage_plans_safe(package: StagedPaperReadinessPackage) -> List[str]:
    warnings = []
    for plan in package.stage_plans:
        warnings.extend(validate_readiness_stage_plan_safety(plan))
    return warnings

def collect_package_safety_flags(package: StagedPaperReadinessPackage) -> List[PromotionDossierRiskFlag]:
    flags = set()
    if validate_package_no_activation(package):
        flags.add(PromotionDossierRiskFlag.READINESS_PACKAGE_ACTIVATION_RISK)
    if validate_package_no_execution_flags(package):
        flags.add(PromotionDossierRiskFlag.REAL_ORDER_RISK)
    return list(flags)

def package_safety_summary(package: StagedPaperReadinessPackage) -> Dict[str, Any]:
    return {
        "activation_warnings": len(validate_package_no_activation(package)),
        "execution_warnings": len(validate_package_no_execution_flags(package)),
        "stage_warnings": len(validate_package_stage_plans_safe(package))
    }

def package_safety_validator_to_text(payload: Dict[str, Any]) -> str:
    total = sum(payload.values())
    if total == 0:
        return "Package Safety Validation PASSED."
    return f"Package Safety Validation FAILED: {total} warnings."
