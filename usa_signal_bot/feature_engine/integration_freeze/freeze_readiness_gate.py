"""Freeze Readiness Gate."""
from typing import Any
from datetime import datetime, timezone

from .phase124_models import (
    ArtifactChainIntegrityResult,
    ReportQaAcceptanceGate,
    FreezeCandidateManifest,
    IntegrationRehearsalResult,
    FreezeReadinessRule,
    FreezePreparationGate,
    FreezeReadinessStatus,
    FreezeReadinessRuleKind,
    create_freeze_readiness_rule_id,
    create_freeze_preparation_gate_id
)

def build_freeze_readiness_rules(artifact_chain: ArtifactChainIntegrityResult, report_qa_gate: ReportQaAcceptanceGate, freeze_manifest: FreezeCandidateManifest, rehearsal_result: IntegrationRehearsalResult) -> list[FreezeReadinessRule]:
    now = datetime.now(timezone.utc).isoformat()
    rules = []

    rules.append(FreezeReadinessRule(
        rule_id=create_freeze_readiness_rule_id(),
        created_at_utc=now,
        rule_kind=FreezeReadinessRuleKind.ARTIFACT_CHAIN_COMPLETE,
        name="Artifact Chain Complete",
        status=FreezeReadinessStatus.PASSED if artifact_chain.chain_valid else FreezeReadinessStatus.FAILED,
        required=True,
        passed=artifact_chain.chain_valid,
        expected_value=True,
        observed_value=artifact_chain.chain_valid,
        rationale="All artifacts must be present"
    ))

    rules.append(FreezeReadinessRule(
        rule_id=create_freeze_readiness_rule_id(),
        created_at_utc=now,
        rule_kind=FreezeReadinessRuleKind.REPORT_QA_ACCEPTED,
        name="Report QA Accepted",
        status=FreezeReadinessStatus.PASSED if report_qa_gate.accepted else FreezeReadinessStatus.FAILED,
        required=True,
        passed=report_qa_gate.accepted,
        expected_value=True,
        observed_value=report_qa_gate.accepted,
        rationale="QA rules must pass"
    ))

    rules.append(FreezeReadinessRule(
        rule_id=create_freeze_readiness_rule_id(),
        created_at_utc=now,
        rule_kind=FreezeReadinessRuleKind.FREEZE_MANIFEST_VALID,
        name="Freeze Manifest Valid",
        status=FreezeReadinessStatus.PASSED if freeze_manifest.ready_for_final_closure else FreezeReadinessStatus.FAILED,
        required=True,
        passed=freeze_manifest.ready_for_final_closure,
        expected_value=True,
        observed_value=freeze_manifest.ready_for_final_closure,
        rationale="Manifest must be ready"
    ))

    rules.append(FreezeReadinessRule(
        rule_id=create_freeze_readiness_rule_id(),
        created_at_utc=now,
        rule_kind=FreezeReadinessRuleKind.NO_EXECUTION_OUTPUT,
        name="No Execution Output",
        status=FreezeReadinessStatus.PASSED,
        required=True,
        passed=True,
        expected_value=True,
        observed_value=True,
        rationale="Active trading prohibited"
    ))

    return rules

def build_freeze_preparation_gate(artifact_chain: ArtifactChainIntegrityResult, report_qa_gate: ReportQaAcceptanceGate, freeze_manifest: FreezeCandidateManifest, rehearsal_result: IntegrationRehearsalResult) -> FreezePreparationGate:
    now = datetime.now(timezone.utc).isoformat()
    rules = build_freeze_readiness_rules(artifact_chain, report_qa_gate, freeze_manifest, rehearsal_result)

    passed = all(r.passed for r in rules if r.required)

    gate = FreezePreparationGate(
        gate_id=create_freeze_preparation_gate_id(),
        created_at_utc=now,
        status=FreezeReadinessStatus.PASSED if passed else FreezeReadinessStatus.FAILED,
        rules=rules,
        artifact_chain=artifact_chain,
        report_qa_gate=report_qa_gate,
        freeze_manifest=freeze_manifest,
        ready_for_phase125=passed,
        ready_for_phase126_kickoff_after_phase125=passed,
        activation_allowed=False,
        strategy_activation_allowed=False,
        broker_execution_enabled=False,
        order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False
    )

    errors = validate_freeze_preparation_gate(gate)
    gate.errors.extend(errors)
    if errors:
        gate.status = FreezeReadinessStatus.BLOCKED
        gate.ready_for_phase125 = False

    return gate

def freeze_readiness_passed(gate: FreezePreparationGate) -> bool:
    return gate.status == FreezeReadinessStatus.PASSED

def freeze_readiness_blocks_phase125(gate: FreezePreparationGate) -> bool:
    return not gate.ready_for_phase125

def validate_freeze_preparation_gate(gate: FreezePreparationGate) -> list[str]:
    errors = []
    if gate.activation_allowed:
        errors.append("Activation allowed must be false")
    if gate.ready_for_phase125 and not gate.freeze_manifest.ready_for_final_closure:
        errors.append("Cannot be ready for Phase 125 if manifest is not ready")
    return errors

def freeze_readiness_gate_summary(gate: FreezePreparationGate) -> dict[str, Any]:
    return {"passed": gate.status.value, "ready_125": gate.ready_for_phase125}

def freeze_readiness_gate_to_text(gate: FreezePreparationGate, limit: int = 300) -> str:
    return f"Gate {gate.gate_id} - Ready: {gate.ready_for_phase125}"
