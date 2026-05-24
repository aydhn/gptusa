import pytest
from usa_signal_bot.runtime_service_graph.phase103_models import (
    RuntimeRegistryIngestionResult,
    RuntimeServiceNode,
    DependencyContract,
    RuntimeServiceGraph,
    SafeOrchestrationPlan,
    OrchestrationDryRunResult,
    validate_runtime_registry_ingestion_result,
    validate_runtime_service_node,
    validate_safe_orchestration_plan,
    validate_orchestration_dry_run_result
)
from usa_signal_bot.core.enums import RuntimeServiceKind, RuntimeServiceStatus, DependencyType, DependencyContractStatus, OrchestrationMode, OrchestrationDecision

def test_ingestion_validation():
    with pytest.raises(ValueError, match="activation_allowed must be false"):
        res = RuntimeRegistryIngestionResult(
            ingestion_id="i", created_at_utc="d", source_path=None, source_review_id=None,
            available=True, registry_normalized=True, provider_interfaces_ready=True,
            safety_policy_valid=True, activation_allowed=True, active_paper_enabled=False,
            broker_execution_enabled=False, paper_state_mutation_enabled=False,
            telegram_real_send_enabled=False, scraping_enabled=False, dashboard_enabled=False,
            valid_for_phase103=False
        )
        validate_runtime_registry_ingestion_result(res)

def test_node_validation():
    with pytest.raises(ValueError, match="execution_allowed must be false"):
        node = RuntimeServiceNode(
            service_id="s", service_name="n", kind=RuntimeServiceKind.UNKNOWN,
            status=RuntimeServiceStatus.UNKNOWN, package_path=None,
            execution_allowed=True
        )
        validate_runtime_service_node(node)

def test_plan_validation():
    with pytest.raises(ValueError, match="dry_run_only must be true"):
        plan = SafeOrchestrationPlan(
            plan_id="p", created_at_utc="d", decision=OrchestrationDecision.UNKNOWN,
            mode=OrchestrationMode.UNKNOWN, graph_id=None, dry_run_only=False
        )
        validate_safe_orchestration_plan(plan)

def test_dry_run_result_validation():
    with pytest.raises(ValueError, match="execution_performed must be false"):
        res = OrchestrationDryRunResult(
            result_id="r", created_at_utc="d", plan_id=None, graph_id=None,
            status="UNKNOWN", execution_performed=True
        )
        validate_orchestration_dry_run_result(res)
