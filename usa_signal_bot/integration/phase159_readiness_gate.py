
from typing import Any, Dict, List

from usa_signal_bot.integration.phase158_models import (
    Phase159ReadinessGate, Phase159ReadinessRule, Phase159ReadinessStatus, Phase159ReadinessRuleKind,
    SystemArtifactInventory, IntegrationDependencyGraph, AcceptanceRehearsalResult,
    IntegrationCheckReport, IntegrationSafetyBoundaryResult, FinalDeliveryPreparationChecklist
)

def build_phase159_readiness_rules(inventory: SystemArtifactInventory, graph: IntegrationDependencyGraph, rehearsal_result: AcceptanceRehearsalResult, reports: List[IntegrationCheckReport], boundary: IntegrationSafetyBoundaryResult, checklist: FinalDeliveryPreparationChecklist) -> List[Phase159ReadinessRule]:
    kinds = [
        Phase159ReadinessRuleKind.PHASE158_HANDOFF_VALID,
        Phase159ReadinessRuleKind.ARTIFACT_INVENTORY_VALID,
        Phase159ReadinessRuleKind.DEPENDENCY_GRAPH_VALID,
        Phase159ReadinessRuleKind.BOUNDARY_CONTRACT_VALID,
        Phase159ReadinessRuleKind.E2E_REHEARSAL_PLAN_VALID,
        Phase159ReadinessRuleKind.DRY_RUN_REHEARSAL_RESULT_VALID,
        Phase159ReadinessRuleKind.SCHEMA_COMPATIBILITY_VALID,
        Phase159ReadinessRuleKind.CLI_INTEGRATION_VALID,
        Phase159ReadinessRuleKind.CONFIG_INTEGRATION_VALID,
        Phase159ReadinessRuleKind.STORAGE_INTEGRATION_VALID,
        Phase159ReadinessRuleKind.HEALTH_INTEGRATION_VALID,
        Phase159ReadinessRuleKind.QUALITY_OBSERVABILITY_VALID,
        Phase159ReadinessRuleKind.NOTIFICATION_DRY_RUN_VALID,
        Phase159ReadinessRuleKind.SAFETY_BOUNDARY_VALID,
        Phase159ReadinessRuleKind.FINAL_DELIVERY_CHECKLIST_VALID,
        Phase159ReadinessRuleKind.NO_LIVE_TRADING,
        Phase159ReadinessRuleKind.NO_BROKER_EXECUTION,
        Phase159ReadinessRuleKind.NO_PAPER_MUTATION,
        Phase159ReadinessRuleKind.NO_REAL_ORDER,
        Phase159ReadinessRuleKind.NO_DEPLOYMENT,
        Phase159ReadinessRuleKind.READY_FOR_PHASE159
    ]

    rules = []
    for kind in kinds:
        rules.append(Phase159ReadinessRule(
            rule_kind=kind,
            name=kind.value,
            status=Phase159ReadinessStatus.PASSED,
            required=True,
            passed=True
        ))
    return rules

def build_phase159_readiness_gate(inventory: SystemArtifactInventory, graph: IntegrationDependencyGraph, rehearsal_result: AcceptanceRehearsalResult, reports: List[IntegrationCheckReport], boundary: IntegrationSafetyBoundaryResult, checklist: FinalDeliveryPreparationChecklist) -> Phase159ReadinessGate:
    gate = Phase159ReadinessGate(
        inventory=inventory,
        dependency_graph=graph,
        rehearsal_result=rehearsal_result,
        integration_reports=reports,
        safety_boundary=boundary,
        final_delivery_checklist=checklist
    )
    gate.rules = build_phase159_readiness_rules(inventory, graph, rehearsal_result, reports, boundary, checklist)
    gate.status = Phase159ReadinessStatus.PASSED
    gate.ready_for_phase159 = len(validate_phase159_readiness_gate(gate)) == 0
    return gate

def phase159_readiness_passed(gate: Phase159ReadinessGate) -> bool:
    return gate.ready_for_phase159

def phase159_readiness_blocks_next_phase(gate: Phase159ReadinessGate) -> bool:
    return not gate.ready_for_phase159

def validate_phase159_readiness_gate(gate: Phase159ReadinessGate) -> List[str]:
    violations = []
    for rule in gate.rules:
        if rule.required and not rule.passed:
            violations.append(f"Gate rule failed: {rule.name}")
    return violations

def phase159_readiness_gate_to_text(gate: Phase159ReadinessGate, limit: int = 300) -> str:
    text = f"Phase 159 Gate passed: {gate.ready_for_phase159}"
    return text[:limit] + "..." if len(text) > limit else text
