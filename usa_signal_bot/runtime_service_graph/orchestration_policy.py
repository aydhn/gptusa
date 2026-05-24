from typing import Any, Dict, List
from usa_signal_bot.runtime_service_graph.phase103_models import RuntimeServiceNode
from usa_signal_bot.core.enums import OrchestrationMode

def build_phase103_orchestration_policy() -> Dict[str, Any]:
    return {
        "dry_run_only": True,
        "metadata_only_default": True,
        "read_only_allowed": True,
        "local_compute_validation_allowed": True,
        "network_allowed": False,
        "execution_allowed": False,
        "broker_allowed": False,
        "order_allowed": False,
        "paper_mutation_allowed": False,
        "telegram_real_send_allowed": False,
        "scraping_allowed": False,
        "dashboard_allowed": False
    }

def resolve_orchestration_mode(service: RuntimeServiceNode) -> OrchestrationMode:
    if service.execution_allowed or service.broker_allowed or service.order_allowed:
        return OrchestrationMode.EXECUTION_DISABLED
    if service.metadata_only:
        return OrchestrationMode.METADATA_ONLY_DRY_RUN
    if service.read_only:
        return OrchestrationMode.READ_ONLY_DRY_RUN
    if service.local_compute_allowed:
        return OrchestrationMode.LOCAL_COMPUTE_DRY_RUN
    return OrchestrationMode.UNKNOWN

def orchestration_policy_allows_service(service: RuntimeServiceNode) -> bool:
    if service.execution_allowed or service.broker_allowed or service.order_allowed:
        return False
    if service.paper_mutation_allowed or service.telegram_real_send_allowed:
        return False
    if service.scraping_allowed or service.dashboard_allowed:
        return False
    return True

def orchestration_policy_blocks_service(service: RuntimeServiceNode) -> bool:
    return not orchestration_policy_allows_service(service)

def validate_orchestration_policy(policy: Dict[str, Any]) -> List[str]:
    errors = []
    if not policy.get("dry_run_only", False):
        errors.append("Policy must enforce dry_run_only")
    if policy.get("execution_allowed", False):
        errors.append("Policy must disable execution")
    if policy.get("network_allowed", False):
        errors.append("Policy must disable network")
    return errors

def orchestration_policy_to_text(policy: Dict[str, Any]) -> str:
    return "Orchestration Policy is valid for Phase 103."
