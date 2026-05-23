from typing import Any, Dict, List
from usa_signal_bot.paper_safe_dossier.paper_safe_dossier_models import NonExecutionAcceptanceSeal
from usa_signal_bot.core.enums import NonExecutionAcceptanceSealStatus

def validate_non_execution_acceptance_seal_safety(seal: NonExecutionAcceptanceSeal) -> List[str]:
    errors = []
    if not seal.sealed:
        errors.append("Seal is not sealed.")
    if not seal.immutable:
        errors.append("Seal is not immutable.")
    if not seal.non_execution_confirmed:
        errors.append("Non-execution not confirmed.")
    if not seal.no_broker_confirmed:
         errors.append("No broker execution not confirmed.")
    if not seal.no_active_paper_confirmed:
         errors.append("No active paper enable not confirmed.")
    if not seal.no_paper_admission_confirmed:
         errors.append("No paper admission not confirmed.")
    if not seal.no_order_confirmed:
         errors.append("No order creation not confirmed.")
    if not seal.no_write_confirmed:
         errors.append("No write not confirmed.")
    if not seal.no_telegram_real_send_confirmed:
         errors.append("No telegram real send not confirmed.")
    if not seal.no_config_patch_confirmed:
         errors.append("No config patch not confirmed.")
    if not seal.seal_is_metadata_only:
         errors.append("Seal is not metadata only.")
    return errors

def non_execution_seal_allows_execution(seal: NonExecutionAcceptanceSeal) -> bool:
    if not seal.non_execution_confirmed or not seal.no_broker_confirmed or not seal.no_active_paper_confirmed:
        return True
    return False

def non_execution_seal_requires_followup(seal: NonExecutionAcceptanceSeal) -> bool:
    return len(seal.required_followups) > 0 or len(seal.warnings) > 0

def non_execution_seal_blocks_next_stage(seal: NonExecutionAcceptanceSeal) -> bool:
    if seal.status in [NonExecutionAcceptanceSealStatus.FAILED, NonExecutionAcceptanceSealStatus.BLOCKED]:
        return True
    return len(validate_non_execution_acceptance_seal_safety(seal)) > 0

def non_execution_seal_validator_summary(seal: NonExecutionAcceptanceSeal) -> Dict[str, Any]:
    errors = validate_non_execution_acceptance_seal_safety(seal)
    return {
        "is_safe": len(errors) == 0,
        "error_count": len(errors),
        "allows_execution": non_execution_seal_allows_execution(seal),
        "blocks_next_stage": non_execution_seal_blocks_next_stage(seal)
    }

def non_execution_seal_validator_to_text(payload: Dict[str, Any]) -> str:
    lines = [f"Is Safe: {payload.get('is_safe', False)}"]
    if payload.get("error_count", 0) > 0:
        lines.append(f"Errors: {payload.get('error_count')}")
    if payload.get("allows_execution", False):
        lines.append("WARNING: Seal allows execution!")
    if payload.get("blocks_next_stage", False):
        lines.append("Status: BLOCKED")
    return "\n".join(lines)
