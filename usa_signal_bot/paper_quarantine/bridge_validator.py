from typing import Any
from pathlib import Path

from usa_signal_bot.core.enums import BridgeOperation
from usa_signal_bot.paper_quarantine.quarantine_models import SupervisedDryRunBridgePlan
from usa_signal_bot.paper_quarantine.output_isolation import validate_quarantine_output_path

def validate_bridge_plan_no_mutation(plan: SupervisedDryRunBridgePlan) -> list[str]:
    errors = []
    if plan.bridge_execution_enabled:
        errors.append("Execution enabled is True")
    if plan.paper_state_mutation_enabled:
        errors.append("Paper state mutation enabled is True")
    if plan.paper_order_enabled:
        errors.append("Paper order enabled is True")
    if plan.broker_order_enabled:
        errors.append("Broker order enabled is True")
    if plan.telegram_real_send_enabled:
        errors.append("Telegram real send enabled is True")
    if plan.production_config_write_enabled:
        errors.append("Production config write enabled is True")
    return errors

def validate_bridge_plan_operations(plan: SupervisedDryRunBridgePlan) -> list[str]:
    errors = []
    forbidden = [
        BridgeOperation.WRITE_PAPER_STATE,
        BridgeOperation.SEND_PAPER_ORDER,
        BridgeOperation.SEND_BROKER_ORDER,
        BridgeOperation.SEND_TELEGRAM_REAL,
        BridgeOperation.WRITE_PRODUCTION_CONFIG,
    ]
    for op in forbidden:
        if op in plan.allowed_operations:
            errors.append(f"Forbidden operation {op.value} is in allowed_operations")
    return errors

def validate_bridge_plan_manual_review(plan: SupervisedDryRunBridgePlan) -> list[str]:
    errors = []
    if not plan.manual_review_required:
        errors.append("Manual review is not required")
    return errors

def validate_bridge_plan_output_isolation(plan: SupervisedDryRunBridgePlan, data_root: Path | None = None) -> list[str]:
    if not plan.quarantine_output_path:
        return ["No output path specified"]
    if data_root:
        return validate_quarantine_output_path(Path(plan.quarantine_output_path), data_root)
    return []

def bridge_validator_summary(plan: SupervisedDryRunBridgePlan) -> dict[str, Any]:
    return {
        "valid_no_mutation": len(validate_bridge_plan_no_mutation(plan)) == 0,
        "valid_operations": len(validate_bridge_plan_operations(plan)) == 0,
    }

def bridge_validator_to_text(payload: dict[str, Any]) -> str:
    lines = [
        "Bridge Plan Validation",
        f"No Mutation: {payload.get('valid_no_mutation')}",
        f"Operations Safe: {payload.get('valid_operations')}"
    ]
    return "\n".join(lines)
