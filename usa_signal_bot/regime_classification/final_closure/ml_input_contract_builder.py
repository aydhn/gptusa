from typing import Any, Dict, List
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
