from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional
import uuid
import datetime
from usa_signal_bot.core.enums import (
    SandboxMountMode, SandboxOperation, SandboxSafetyFlag,
    SandboxActivationStatus, SandboxRuntimeMode, SandboxValidationStatus,
    SandboxStatus, SandboxReportType
)

@dataclass
class SandboxMountPlan:
    mount_id: str
    created_at_utc: str
    bundle_id: Optional[str]
    bundle_version: Optional[str]
    mount_mode: SandboxMountMode
    source_bundle_path: Optional[str]
    sandbox_output_path: Optional[str]
    read_only_verified: bool
    copy_on_write_enabled: bool
    allowed_operations: List[SandboxOperation]
    denied_operations: List[SandboxOperation]
    safety_flags: List[SandboxSafetyFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SandboxActivationPlan:
    activation_id: str
    created_at_utc: str
    bundle_id: Optional[str]
    bundle_version: Optional[str]
    status: SandboxActivationStatus
    mount_plan: Optional[SandboxMountPlan]
    bundle_validation_summary: Dict[str, Any]
    compatibility_summary: Dict[str, Any]
    safety_summary: Dict[str, Any]
    runtime_mode: SandboxRuntimeMode
    manual_review_required: bool
    allowed_for_production_apply: bool
    allowed_for_order_routing: bool
    allowed_for_paper_state_mutation: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SandboxRuntimeContext:
    context_id: str
    created_at_utc: str
    sandbox_id: Optional[str]
    bundle_id: Optional[str]
    bundle_version: Optional[str]
    runtime_mode: SandboxRuntimeMode
    in_memory_config: Dict[str, Any]
    mounted_artifacts: List[Dict[str, Any]]
    sandbox_output_path: Optional[str]
    allowed_operations: List[SandboxOperation]
    denied_operations: List[SandboxOperation]
    allowed_to_write_production_config: bool
    allowed_to_mutate_paper_state: bool
    allowed_to_send_orders: bool
    allowed_to_send_telegram_real: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SandboxPreviewOutput:
    output_id: str
    created_at_utc: str
    output_type: str
    status: SandboxValidationStatus
    summary: Dict[str, Any]
    payload: Dict[str, Any]
    safety_flags: List[SandboxSafetyFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SandboxPreviewRun:
    run_id: str
    created_at_utc: str
    sandbox_id: Optional[str]
    bundle_id: Optional[str]
    bundle_version: Optional[str]
    runtime_mode: SandboxRuntimeMode
    status: SandboxStatus
    context: Optional[SandboxRuntimeContext]
    outputs: List[SandboxPreviewOutput]
    operation_decisions: List[Dict[str, Any]]
    safety_flags: List[SandboxSafetyFlag]
    started_at_utc: Optional[str]
    completed_at_utc: Optional[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SandboxValidationResult:
    validation_id: str
    created_at_utc: str
    sandbox_id: Optional[str]
    bundle_id: Optional[str]
    status: SandboxValidationStatus
    safety_flags: List[SandboxSafetyFlag]
    read_only_passed: bool
    output_isolation_passed: bool
    blocked_operations_enforced: bool
    no_order_routing_passed: bool
    no_paper_mutation_passed: bool
    no_telegram_real_send_passed: bool
    validation_messages: List[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ReleaseSandboxReview:
    review_id: str
    created_at_utc: str
    report_type: SandboxReportType
    activation_plans: List[SandboxActivationPlan]
    mount_plans: List[SandboxMountPlan]
    preview_runs: List[SandboxPreviewRun]
    validation_results: List[SandboxValidationResult]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

from usa_signal_bot.core.exceptions import ReleaseSandboxError

def create_sandbox_mount_plan_id(prefix: str = "sandbox_mount") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_sandbox_activation_plan_id(prefix: str = "sandbox_activation") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_sandbox_runtime_context_id(prefix: str = "sandbox_context") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_sandbox_preview_output_id(prefix: str = "sandbox_output") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_sandbox_preview_run_id(prefix: str = "sandbox_run") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_sandbox_validation_result_id(prefix: str = "sandbox_validation") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_release_sandbox_review_id(prefix: str = "release_sandbox_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def validate_sandbox_mount_plan(item: SandboxMountPlan) -> None:
    if SandboxOperation.WRITE_PRODUCTION_CONFIG in item.allowed_operations:
        raise ReleaseSandboxError("WRITE_PRODUCTION_CONFIG cannot be allowed")
    if SandboxOperation.MUTATE_PAPER_STATE in item.allowed_operations:
        raise ReleaseSandboxError("MUTATE_PAPER_STATE cannot be allowed")
    if SandboxOperation.SEND_ORDER in item.allowed_operations:
        raise ReleaseSandboxError("SEND_ORDER cannot be allowed")
    if SandboxOperation.SEND_TELEGRAM_REAL in item.allowed_operations:
        raise ReleaseSandboxError("SEND_TELEGRAM_REAL cannot be allowed")

def validate_sandbox_activation_plan(item: SandboxActivationPlan) -> None:
    if item.allowed_for_production_apply:
        raise ReleaseSandboxError("allowed_for_production_apply must be False")
    if item.allowed_for_order_routing:
        raise ReleaseSandboxError("allowed_for_order_routing must be False")
    if item.allowed_for_paper_state_mutation:
        raise ReleaseSandboxError("allowed_for_paper_state_mutation must be False")

def validate_sandbox_runtime_context(item: SandboxRuntimeContext) -> None:
    if item.allowed_to_write_production_config:
        raise ReleaseSandboxError("allowed_to_write_production_config must be False")
    if item.allowed_to_mutate_paper_state:
        raise ReleaseSandboxError("allowed_to_mutate_paper_state must be False")
    if item.allowed_to_send_orders:
        raise ReleaseSandboxError("allowed_to_send_orders must be False")
    if item.allowed_to_send_telegram_real:
        raise ReleaseSandboxError("allowed_to_send_telegram_real must be False")

def validate_sandbox_preview_run(item: SandboxPreviewRun) -> None:
    if item.context:
        validate_sandbox_runtime_context(item.context)

def validate_sandbox_validation_result(item: SandboxValidationResult) -> None:
    pass

def validate_release_sandbox_review(item: ReleaseSandboxReview) -> None:
    for p in item.activation_plans:
        validate_sandbox_activation_plan(p)

def sandbox_mount_plan_to_dict(item: SandboxMountPlan) -> dict: return item.__dict__
def sandbox_activation_plan_to_dict(item: SandboxActivationPlan) -> dict: return item.__dict__
def sandbox_runtime_context_to_dict(item: SandboxRuntimeContext) -> dict: return item.__dict__
def sandbox_preview_output_to_dict(item: SandboxPreviewOutput) -> dict: return item.__dict__
def sandbox_preview_run_to_dict(item: SandboxPreviewRun) -> dict: return item.__dict__
def sandbox_validation_result_to_dict(item: SandboxValidationResult) -> dict: return item.__dict__
def release_sandbox_review_to_dict(item: ReleaseSandboxReview) -> dict: return item.__dict__
