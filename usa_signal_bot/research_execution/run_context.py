from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.core.enums import ResearchRunType, ExperimentExecutionMode
from usa_signal_bot.research_execution.execution_models import ExperimentRunContext, ConfigSnapshot, create_experiment_run_context_id

def build_baseline_run_context(experiment_plan: dict[str, Any], baseline_snapshot: ConfigSnapshot, execution_mode: ExperimentExecutionMode = ExperimentExecutionMode.MOCK_ONLY) -> ExperimentRunContext:
    context = ExperimentRunContext(
        context_id=create_experiment_run_context_id("baseline_ctx"),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        experiment_id=experiment_plan.get("experiment_id"),
        hypothesis_id=experiment_plan.get("hypothesis_id"),
        run_type=ResearchRunType.BASELINE,
        execution_mode=execution_mode,
        config_snapshot=baseline_snapshot,
        validation_plan=experiment_plan.get("validation_plan", {}),
        acceptance_gates=experiment_plan.get("acceptance_gates", []),
        data_scope=build_data_scope_from_validation_plan(experiment_plan.get("validation_plan", {})),
        allowed_to_modify_config=False,
        allowed_to_send_orders=False,
        warnings=[],
        errors=[],
        metadata={}
    )
    warnings = validate_run_context_safety(context)
    context.warnings.extend(warnings)
    return context

def build_candidate_run_context(experiment_plan: dict[str, Any], candidate_snapshot: ConfigSnapshot, execution_mode: ExperimentExecutionMode = ExperimentExecutionMode.MOCK_ONLY) -> ExperimentRunContext:
    context = ExperimentRunContext(
        context_id=create_experiment_run_context_id("candidate_ctx"),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        experiment_id=experiment_plan.get("experiment_id"),
        hypothesis_id=experiment_plan.get("hypothesis_id"),
        run_type=ResearchRunType.CANDIDATE,
        execution_mode=execution_mode,
        config_snapshot=candidate_snapshot,
        validation_plan=experiment_plan.get("validation_plan", {}),
        acceptance_gates=experiment_plan.get("acceptance_gates", []),
        data_scope=build_data_scope_from_validation_plan(experiment_plan.get("validation_plan", {})),
        allowed_to_modify_config=False,
        allowed_to_send_orders=False,
        warnings=[],
        errors=[],
        metadata={}
    )
    warnings = validate_run_context_safety(context)
    context.warnings.extend(warnings)
    return context

def build_data_scope_from_validation_plan(validation_plan: dict[str, Any]) -> dict[str, Any]:
    return validation_plan.get("data_scope", {"start_date": "2020-01-01", "end_date": "2023-12-31", "symbols": ["SPY"]})

def validate_run_context_safety(context: ExperimentRunContext) -> list[str]:
    warnings = []
    if context.allowed_to_modify_config:
        warnings.append("SAFETY VIOLATION: Run context allowed_to_modify_config is True. Forcing to False.")
        context.allowed_to_modify_config = False

    if context.allowed_to_send_orders:
        warnings.append("SAFETY VIOLATION: Run context allowed_to_send_orders is True. Forcing to False.")
        context.allowed_to_send_orders = False

    return warnings

def run_context_to_text(context: ExperimentRunContext) -> str:
    lines = [f"--- RUN CONTEXT: {context.context_id} ---"]
    lines.append(f"Run Type: {context.run_type.value}")
    lines.append(f"Execution Mode: {context.execution_mode.value}")
    lines.append(f"Allowed to send orders: {context.allowed_to_send_orders}")
    lines.append(f"Allowed to modify config: {context.allowed_to_modify_config}")
    lines.append("NOTE: Context strictly enforced for local, disconnected analytics.")
    return "\n".join(lines)
