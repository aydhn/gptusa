from typing import Any, Dict, List
from usa_signal_bot.regime_classification.final_closure.phase135_models import (
    RegimeFinalClosureResult,
    RegimeFreezeSeal,
    RegimeFinalSafetyAudit,
    MLInputContract,
    MLKickoffReadinessGate,
    MLKickoffReadinessRule,
    MLKickoffReadinessRuleKind,
    MLKickoffReadinessStatus,
    create_ml_kickoff_readiness_gate_id,
    create_ml_kickoff_readiness_rule_id
)
from datetime import datetime, timezone

def build_ml_kickoff_readiness_rules(
    closure_result: RegimeFinalClosureResult,
    seal: RegimeFreezeSeal,
    audit: RegimeFinalSafetyAudit,
    contract: MLInputContract
) -> List[MLKickoffReadinessRule]:

    passed = closure_result.closure_passed and audit.safety_passed and contract.contract_valid

    return [
        MLKickoffReadinessRule(
            rule_id=create_ml_kickoff_readiness_rule_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            rule_kind=MLKickoffReadinessRuleKind.REGIME_FINAL_CLOSURE_VALID,
            name="Regime Final Closure Valid",
            status=MLKickoffReadinessStatus.PASSED if passed else MLKickoffReadinessStatus.FAILED,
            required=True,
            passed=passed
        )
    ]

def build_ml_kickoff_readiness_gate(
    closure_result: RegimeFinalClosureResult,
    seal: RegimeFreezeSeal,
    audit: RegimeFinalSafetyAudit,
    contract: MLInputContract
) -> MLKickoffReadinessGate:

    rules = build_ml_kickoff_readiness_rules(closure_result, seal, audit, contract)
    passed = all(r.passed for r in rules)

    return MLKickoffReadinessGate(
        gate_id=create_ml_kickoff_readiness_gate_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=MLKickoffReadinessStatus.PASSED if passed else MLKickoffReadinessStatus.FAILED,
        rules=rules,
        input_contract=contract,
        freeze_seal=seal,
        final_safety_audit=audit,
        ready_for_phase136=passed
    )

def ml_kickoff_readiness_passed(gate: MLKickoffReadinessGate) -> bool:
    return gate.status == MLKickoffReadinessStatus.PASSED

def ml_kickoff_readiness_blocks_phase136(gate: MLKickoffReadinessGate) -> bool:
    return not gate.ready_for_phase136

def validate_ml_kickoff_readiness_gate(gate: MLKickoffReadinessGate) -> List[str]:
    return []

def ml_kickoff_readiness_gate_summary(gate: MLKickoffReadinessGate) -> Dict[str, Any]:
    return {"status": gate.status.name}

def ml_kickoff_readiness_gate_to_text(gate: MLKickoffReadinessGate, limit: int = 300) -> str:
    return f"Gate Status: {gate.status.name}"
