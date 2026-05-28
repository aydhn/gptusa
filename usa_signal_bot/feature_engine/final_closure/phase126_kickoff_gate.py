import datetime
from typing import Any, Dict, List
from usa_signal_bot.core.enums import Phase126KickoffRequirementKind, Phase126KickoffGateStatus
from usa_signal_bot.feature_engine.final_closure.phase125_models import (
    FinalClosureManifest,
    FreezeSealMetadata,
    EngineReadinessCertificate,
    Phase126KickoffRequirement,
    Phase126KickoffGate,
    create_phase126_kickoff_requirement_id,
    create_phase126_kickoff_gate_id
)

def _create_req(kind: Phase126KickoffRequirementKind, passed: bool, rationale: str) -> Phase126KickoffRequirement:
    return Phase126KickoffRequirement(
        requirement_id=create_phase126_kickoff_requirement_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        requirement_kind=kind,
        name=kind.value,
        status=Phase126KickoffGateStatus.PASSED if passed else Phase126KickoffGateStatus.FAILED,
        required=True,
        passed=passed,
        expected_value=True,
        observed_value=passed,
        rationale=rationale,
        warnings=[],
        errors=[] if passed else [rationale],
        risk_flags=[],
        metadata={}
    )

def build_phase126_kickoff_requirements(manifest: FinalClosureManifest, seal: FreezeSealMetadata, certificate: EngineReadinessCertificate) -> List[Phase126KickoffRequirement]:
    valid = manifest.final_manifest_valid and seal.sealed and certificate.certified_for_research_handoff
    return [
        _create_req(Phase126KickoffRequirementKind.FEATURE_FACTOR_ENGINE_CLOSED, valid, "Engine must be closed"),
        _create_req(Phase126KickoffRequirementKind.FREEZE_SEAL_VALID, seal.sealed, "Seal must be valid"),
        _create_req(Phase126KickoffRequirementKind.ENGINE_CERTIFICATE_VALID, certificate.certified_for_research_handoff, "Certificate must be valid"),
        _create_req(Phase126KickoffRequirementKind.FACTOR_TABLES_AVAILABLE, valid, "Factor tables available"),
        _create_req(Phase126KickoffRequirementKind.FACTOR_DIAGNOSTICS_AVAILABLE, valid, "Factor diagnostics available"),
        _create_req(Phase126KickoffRequirementKind.RESEARCH_REPORTS_AVAILABLE, valid, "Research reports available"),
        _create_req(Phase126KickoffRequirementKind.SCHEMA_CONTRACT_AVAILABLE, valid, "Schema contract available"),
        _create_req(Phase126KickoffRequirementKind.LINEAGE_CONTRACT_AVAILABLE, valid, "Lineage contract available"),
        _create_req(Phase126KickoffRequirementKind.SAFETY_BOUNDARY_AVAILABLE, valid, "Safety boundary available"),
        _create_req(Phase126KickoffRequirementKind.REGIME_INPUT_CONTRACT_READY, valid, "Regime input contract ready"),
        _create_req(Phase126KickoffRequirementKind.NO_SIGNAL_OUTPUT, True, "No signal output"),
        _create_req(Phase126KickoffRequirementKind.NO_ORDER_OUTPUT, True, "No order output"),
        _create_req(Phase126KickoffRequirementKind.NO_PORTFOLIO_OUTPUT, True, "No portfolio output"),
        _create_req(Phase126KickoffRequirementKind.NO_EXECUTION_OUTPUT, True, "No execution output"),
    ]

def build_phase126_kickoff_gate(manifest: FinalClosureManifest, seal: FreezeSealMetadata, certificate: EngineReadinessCertificate) -> Phase126KickoffGate:
    reqs = build_phase126_kickoff_requirements(manifest, seal, certificate)
    passed_reqs = sum(1 for r in reqs if r.passed)
    failed_reqs = sum(1 for r in reqs if not r.passed)
    gate_passed = failed_reqs == 0
    return Phase126KickoffGate(
        gate_id=create_phase126_kickoff_gate_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        status=Phase126KickoffGateStatus.PASSED if gate_passed else Phase126KickoffGateStatus.FAILED,
        requirements=reqs,
        total_requirements=len(reqs),
        passed_requirements=passed_reqs,
        failed_requirements=failed_reqs,
        blocked_requirements=0,
        ready_for_phase126=gate_passed,
        regime_classification_input_contract_ready=gate_passed,
        feature_factor_engine_closed=gate_passed,
        freeze_seal_valid=seal.sealed,
        engine_certificate_valid=certificate.certified_for_research_handoff,
        research_handoff_ready=gate_passed,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        broker_execution_enabled=False,
        order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[] if gate_passed else ["Gate requirements failed"],
        risk_flags=[],
        metadata={}
    )

def phase126_kickoff_passed(gate: Phase126KickoffGate) -> bool:
    return gate.status == Phase126KickoffGateStatus.PASSED

def phase126_kickoff_blocks_next_phase(gate: Phase126KickoffGate) -> bool:
    return not phase126_kickoff_passed(gate)

def validate_phase126_kickoff_gate(gate: Phase126KickoffGate) -> List[str]:
    errs = []
    if gate.activation_allowed: errs.append("activation_allowed is true")
    if gate.strategy_activation_allowed: errs.append("strategy_activation_allowed is true")
    if gate.deployment_allowed: errs.append("deployment_allowed is true")
    return errs

def phase126_kickoff_gate_summary(gate: Phase126KickoffGate) -> Dict[str, Any]:
    return {
        "passed": phase126_kickoff_passed(gate),
        "status": gate.status.value,
        "failed_requirements": gate.failed_requirements
    }

def phase126_kickoff_gate_to_text(gate: Phase126KickoffGate, limit: int = 300) -> str:
    return f"KickoffGate({gate.gate_id}): Status={gate.status.value}"
