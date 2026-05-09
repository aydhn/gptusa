from dataclasses import dataclass, field
from typing import Any
import uuid
import datetime
from usa_signal_bot.core.enums import RecoveryActionType, RecoveryActionStatus, RecoveryPlanStatus
from usa_signal_bot.core.exceptions import RecoveryActionError

@dataclass
class RecoveryAction:
    action_id: str
    action_type: RecoveryActionType
    name: str
    description: str
    command: str | None
    dry_run: bool
    required: bool
    status: RecoveryActionStatus
    safety_note: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RecoveryActionResult:
    action_id: str
    action_type: RecoveryActionType
    status: RecoveryActionStatus
    executed_at_utc: str
    dry_run: bool
    summary: str
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

@dataclass
class RecoveryPlan:
    plan_id: str
    created_at_utc: str
    status: RecoveryPlanStatus
    incident_ids: list[str]
    actions: list[RecoveryAction]
    required_action_count: int
    dry_run: bool
    warnings: list[str]
    errors: list[str]

@dataclass
class RecoveryPlanResult:
    result_id: str
    created_at_utc: str
    status: RecoveryPlanStatus
    plan: RecoveryPlan
    action_results: list[RecoveryActionResult]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

def create_recovery_action_id(name: str) -> str:
    return f"act_{name.replace(' ', '_').lower()}_{uuid.uuid4().hex[:6]}"

def create_recovery_plan_id(prefix: str = "recovery_plan") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_recovery_plan_result_id(prefix: str = "recovery_result") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def validate_recovery_action(action: RecoveryAction) -> None:
    if not action.name:
         raise RecoveryActionError("Action name cannot be empty")
    if not action.description:
         raise RecoveryActionError("Action description cannot be empty")

def validate_recovery_plan(plan: RecoveryPlan) -> None:
    for act in plan.actions:
        validate_recovery_action(act)

def recovery_action_to_dict(action: RecoveryAction) -> dict:
    return {
        "action_id": action.action_id,
        "action_type": action.action_type.value,
        "name": action.name,
        "description": action.description,
        "command": action.command,
        "dry_run": action.dry_run,
        "required": action.required,
        "status": action.status.value,
        "safety_note": action.safety_note,
        "metadata": action.metadata
    }

def recovery_action_result_to_dict(result: RecoveryActionResult) -> dict:
    return {
        "action_id": result.action_id,
        "action_type": result.action_type.value,
        "status": result.status.value,
        "executed_at_utc": result.executed_at_utc,
        "dry_run": result.dry_run,
        "summary": result.summary,
        "output_paths": result.output_paths,
        "warnings": result.warnings,
        "errors": result.errors
    }

def recovery_plan_to_dict(plan: RecoveryPlan) -> dict:
    return {
        "plan_id": plan.plan_id,
        "created_at_utc": plan.created_at_utc,
        "status": plan.status.value,
        "incident_ids": plan.incident_ids,
        "actions": [recovery_action_to_dict(a) for a in plan.actions],
        "required_action_count": plan.required_action_count,
        "dry_run": plan.dry_run,
        "warnings": plan.warnings,
        "errors": plan.errors
    }

def recovery_plan_result_to_dict(result: RecoveryPlanResult) -> dict:
    return {
        "result_id": result.result_id,
        "created_at_utc": result.created_at_utc,
        "status": result.status.value,
        "plan": recovery_plan_to_dict(result.plan),
        "action_results": [recovery_action_result_to_dict(r) for r in result.action_results],
        "output_paths": result.output_paths,
        "warnings": result.warnings,
        "errors": result.errors
    }
