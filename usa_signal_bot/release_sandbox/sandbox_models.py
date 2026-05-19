from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict
import datetime
import uuid

from usa_signal_bot.core.enums import (
    SandboxStatus, SandboxActivationStatus, SandboxMountMode, SandboxRuntimeMode,
    SandboxOperation, SandboxSafetyFlag, SandboxValidationStatus, SandboxReportType
)
from usa_signal_bot.core.exceptions import ReleaseSandboxValidationError

def _now_str() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

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


def sandbox_mount_plan_to_dict(item: SandboxMountPlan) -> dict:
    from dataclasses import asdict
    return asdict(item)

def sandbox_activation_plan_to_dict(item: SandboxActivationPlan) -> dict:
    from dataclasses import asdict
    return asdict(item)

def sandbox_runtime_context_to_dict(item: SandboxRuntimeContext) -> dict:
    from dataclasses import asdict
    return asdict(item)

def sandbox_preview_output_to_dict(item: SandboxPreviewOutput) -> dict:
    from dataclasses import asdict
    return asdict(item)

def sandbox_preview_run_to_dict(item: SandboxPreviewRun) -> dict:
    from dataclasses import asdict
    return asdict(item)

def sandbox_validation_result_to_dict(item: SandboxValidationResult) -> dict:
    from dataclasses import asdict
    return asdict(item)

def release_sandbox_review_to_dict(item: ReleaseSandboxReview) -> dict:
    from dataclasses import asdict
    return asdict(item)


def validate_sandbox_mount_plan(item: SandboxMountPlan) -> None:
    pass

def validate_sandbox_activation_plan(item: SandboxActivationPlan) -> None:
    if item.allowed_for_production_apply:
        raise ReleaseSandboxValidationError("allowed_for_production_apply must be False")
    if item.allowed_for_order_routing:
        raise ReleaseSandboxValidationError("allowed_for_order_routing must be False")
    if item.allowed_for_paper_state_mutation:
        raise ReleaseSandboxValidationError("allowed_for_paper_state_mutation must be False")

def validate_sandbox_runtime_context(item: SandboxRuntimeContext) -> None:
    if item.allowed_to_write_production_config:
        raise ReleaseSandboxValidationError("allowed_to_write_production_config must be False")
    if item.allowed_to_mutate_paper_state:
        raise ReleaseSandboxValidationError("allowed_to_mutate_paper_state must be False")
    if item.allowed_to_send_orders:
        raise ReleaseSandboxValidationError("allowed_to_send_orders must be False")
    if item.allowed_to_send_telegram_real:
        raise ReleaseSandboxValidationError("allowed_to_send_telegram_real must be False")

    bad_ops = [SandboxOperation.WRITE_PRODUCTION_CONFIG, SandboxOperation.MUTATE_PAPER_STATE,
               SandboxOperation.SEND_ORDER, SandboxOperation.SEND_TELEGRAM_REAL]
    for op in bad_ops:
        if op in item.allowed_operations:
            raise ReleaseSandboxValidationError(f"{op.value} cannot be in allowed_operations")

def validate_sandbox_preview_run(item: SandboxPreviewRun) -> None:
    pass

def validate_sandbox_validation_result(item: SandboxValidationResult) -> None:
    pass

def validate_release_sandbox_review(item: ReleaseSandboxReview) -> None:
    pass


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
