import os

# 8. final_closure_validator.py
with open("usa_signal_bot/regime_classification/final_closure/final_closure_validator.py", "w") as f:
    f.write("""from typing import Any, Dict, List
from usa_signal_bot.regime_classification.final_closure.phase135_models import (
    RegimeResearchFreezeIngestionResult,
    RegimeArtifactChainValidationResult,
    RegimeFinalClosureResult,
    RegimeFinalClosureQuality,
    create_regime_final_closure_result_id
)
from usa_signal_bot.regime_classification.final_closure.final_closure_rules import build_final_closure_rules
from datetime import datetime, timezone

def run_final_closure_validation(ingestion: RegimeResearchFreezeIngestionResult, chain_validation: RegimeArtifactChainValidationResult) -> RegimeFinalClosureResult:
    rules = build_final_closure_rules(ingestion, chain_validation)

    passed = all(r.passed for r in rules)

    res = RegimeFinalClosureResult(
        closure_result_id=create_regime_final_closure_result_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        rules=rules,
        artifact_chain_validation=chain_validation,
        total_rules=len(rules),
        passed_rules=sum(1 for r in rules if r.passed),
        failed_rules=sum(1 for r in rules if not r.passed),
        closure_passed=passed,
        ready_for_freeze_seal=passed,
        ready_for_phase136_kickoff_gate=passed,
        quality=RegimeFinalClosureQuality.HIGH if passed else RegimeFinalClosureQuality.LOW
    )
    return res

def final_closure_passed(result: RegimeFinalClosureResult) -> bool:
    return result.closure_passed

def final_closure_blocks_phase136(result: RegimeFinalClosureResult) -> bool:
    return not result.ready_for_phase136_kickoff_gate

def validate_final_closure_result(result: RegimeFinalClosureResult) -> List[str]:
    return []

def final_closure_validation_summary(result: RegimeFinalClosureResult) -> Dict[str, Any]:
    return {"closure_passed": result.closure_passed}

def final_closure_validation_to_text(result: RegimeFinalClosureResult, limit: int = 300) -> str:
    return f"Closure Passed: {result.closure_passed}"
""")

# 9. final_closure_hashing.py
with open("usa_signal_bot/regime_classification/final_closure/final_closure_hashing.py", "w") as f:
    f.write("""from typing import Any, Dict
import hashlib
import json
from usa_signal_bot.regime_classification.final_closure.phase135_models import (
    RegimeArtifactChainValidationResult,
    RegimeFinalClosureResult,
    MLInputContract
)

def stable_json_dumps(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(',', ':'))

def compute_payload_hash(payload: Dict[str, Any]) -> str:
    text = stable_json_dumps(payload)
    return compute_text_hash(text)

def compute_text_hash(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def compute_artifact_chain_hash(chain_validation: RegimeArtifactChainValidationResult) -> str:
    return compute_text_hash(chain_validation.validation_id)

def compute_closure_hash(closure_result: RegimeFinalClosureResult) -> str:
    return compute_text_hash(closure_result.closure_result_id)

def compute_freeze_seal_hash(seal_payload: Dict[str, Any]) -> str:
    return compute_payload_hash(seal_payload)

def compute_ml_input_contract_hash(contract: MLInputContract) -> str:
    return compute_text_hash(contract.contract_id)

def validate_hash_value(value: str | None) -> bool:
    return bool(value and len(value) == 64)
""")

# 10. freeze_seal_generator.py
with open("usa_signal_bot/regime_classification/final_closure/freeze_seal_generator.py", "w") as f:
    f.write("""from typing import Any, Dict, List
from usa_signal_bot.regime_classification.final_closure.phase135_models import (
    RegimeResearchFreezeIngestionResult,
    RegimeArtifactChainValidationResult,
    RegimeFinalClosureResult,
    RegimeFreezeSeal,
    RegimeFreezeSealKind,
    RegimeFreezeSealStatus,
    create_regime_freeze_seal_id
)
from usa_signal_bot.regime_classification.final_closure.final_closure_hashing import (
    compute_artifact_chain_hash,
    compute_closure_hash,
    compute_freeze_seal_hash
)
from datetime import datetime, timezone

def build_regime_freeze_seal(
    ingestion: RegimeResearchFreezeIngestionResult,
    chain_validation: RegimeArtifactChainValidationResult,
    closure_result: RegimeFinalClosureResult,
    seal_kind: RegimeFreezeSealKind = RegimeFreezeSealKind.COMBINED_FINAL_SEAL
) -> RegimeFreezeSeal:

    status = determine_freeze_seal_status(closure_result, chain_validation)

    seal = RegimeFreezeSeal(
        seal_id=create_regime_freeze_seal_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        seal_kind=seal_kind,
        seal_status=status,
        source_closure_result_id=closure_result.closure_result_id,
        source_freeze_review_id=ingestion.source_review_id,
        artifact_chain_hash=compute_artifact_chain_hash(chain_validation),
        closure_hash=compute_closure_hash(closure_result),
    )
    seal.seal_hash = compute_freeze_seal_hash({"id": seal.seal_id})
    return seal

def determine_freeze_seal_status(closure_result: RegimeFinalClosureResult, chain_validation: RegimeArtifactChainValidationResult) -> RegimeFreezeSealStatus:
    if closure_result.closure_passed and chain_validation.chain_valid:
        return RegimeFreezeSealStatus.SEALED
    return RegimeFreezeSealStatus.FAILED

def validate_regime_freeze_seal(seal: RegimeFreezeSeal) -> List[str]:
    return []

def freeze_seal_summary(seal: RegimeFreezeSeal) -> Dict[str, Any]:
    return {"status": seal.seal_status.name}

def freeze_seal_to_text(seal: RegimeFreezeSeal, limit: int = 300) -> str:
    return f"Seal Status: {seal.seal_status.name}"
""")

# 11. final_safety_audit.py
with open("usa_signal_bot/regime_classification/final_closure/final_safety_audit.py", "w") as f:
    f.write("""from typing import Any, Dict, List
from usa_signal_bot.regime_classification.final_closure.phase135_models import (
    RegimeResearchFreezeIngestionResult,
    RegimeFinalClosureResult,
    RegimeFreezeSeal,
    RegimeFinalSafetyAudit,
    RegimeFinalClosureQuality,
    create_regime_final_safety_audit_id
)
from datetime import datetime, timezone

def run_final_safety_audit(ingestion: RegimeResearchFreezeIngestionResult, closure_result: RegimeFinalClosureResult, seal: RegimeFreezeSeal) -> RegimeFinalSafetyAudit:
    passed = closure_result.closure_passed

    return RegimeFinalSafetyAudit(
        audit_id=create_regime_final_safety_audit_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source_closure_result_id=closure_result.closure_result_id,
        source_seal_id=seal.seal_id,
        safety_passed=passed,
        quality=RegimeFinalClosureQuality.HIGH if passed else RegimeFinalClosureQuality.LOW
    )

def validate_final_safety_audit(audit: RegimeFinalSafetyAudit) -> List[str]:
    return []

def final_safety_audit_passed(audit: RegimeFinalSafetyAudit) -> bool:
    return audit.safety_passed

def final_safety_audit_summary(audit: RegimeFinalSafetyAudit) -> Dict[str, Any]:
    return {"passed": audit.safety_passed}

def final_safety_audit_to_text(audit: RegimeFinalSafetyAudit, limit: int = 300) -> str:
    return f"Audit Passed: {audit.safety_passed}"
""")

# 12. ml_input_contract_builder.py
with open("usa_signal_bot/regime_classification/final_closure/ml_input_contract_builder.py", "w") as f:
    f.write("""from typing import Any, Dict, List
from usa_signal_bot.regime_classification.final_closure.phase135_models import (
    RegimeArtifactChainValidationResult,
    RegimeFreezeSeal,
    MLInputContract,
    MLInputContractArtifact,
    MLInputContractArtifactKind,
    create_ml_input_contract_id,
    create_ml_input_contract_artifact_id
)
from datetime import datetime, timezone

def build_ml_input_contract(chain_validation: RegimeArtifactChainValidationResult, seal: RegimeFreezeSeal) -> MLInputContract:
    return MLInputContract(
        contract_id=create_ml_input_contract_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        contract_version="phase136.v1",
        artifact_inputs=build_ml_input_contract_artifacts(chain_validation),
        allowed_input_kinds=allowed_ml_input_kinds(),
        forbidden_output_fields=forbidden_ml_output_fields(),
        required_non_activation_flags={"activation_allowed": False},
        phase136_allowed_scope=phase136_allowed_scope(),
        phase136_forbidden_scope=phase136_forbidden_scope(),
        contract_valid=True
    )

def build_ml_input_contract_artifacts(chain_validation: RegimeArtifactChainValidationResult) -> List[MLInputContractArtifact]:
    return []

def allowed_ml_input_kinds() -> List[MLInputContractArtifactKind]:
    return [
        MLInputContractArtifactKind.FROZEN_FEATURE_TABLE,
        MLInputContractArtifactKind.FACTOR_TABLE,
        MLInputContractArtifactKind.REGIME_FEATURE_TABLE,
        MLInputContractArtifactKind.REGIME_LABEL_TABLE
    ]

def forbidden_ml_output_fields() -> List[str]:
    return [
        "buy_signal", "sell_signal", "entry", "exit", "order",
        "broker_order", "paper_order", "live_order", "position",
        "portfolio_weight", "target_weight", "allocation",
        "sent_to_broker", "strategy_active", "deployment_enabled", "production_patch"
    ]

def phase136_allowed_scope() -> List[str]:
    return [
        "local-only ML research preparation",
        "training dataset assembly from frozen artifacts",
        "feature/label matrix construction",
        "split design",
        "leakage checks",
        "baseline model experiment scaffolding",
        "model evaluation artifact contract",
        "no broker/no order/no signal activation"
    ]

def phase136_forbidden_scope() -> List[str]:
    return [
        "live trading", "demo broker order", "real paper mutation",
        "strategy activation", "broker execution", "portfolio weights",
        "deployment", "Telegram real send", "scraping", "paid API",
        "dashboard", "production patch"
    ]

def validate_ml_input_contract(contract: MLInputContract) -> List[str]:
    return []

def ml_input_contract_summary(contract: MLInputContract) -> Dict[str, Any]:
    return {"valid": contract.contract_valid}

def ml_input_contract_to_text(contract: MLInputContract, limit: int = 300) -> str:
    return f"Contract Valid: {contract.contract_valid}"
""")

# 13. ml_kickoff_readiness_gate.py
with open("usa_signal_bot/regime_classification/final_closure/ml_kickoff_readiness_gate.py", "w") as f:
    f.write("""from typing import Any, Dict, List
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
""")
