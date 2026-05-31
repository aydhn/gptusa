from typing import Any, Dict, List
from datetime import datetime, timezone
import hashlib
from .phase136_models import MLDatasetContract, MLDatasetContractKind, MLFoundationQuality, create_ml_dataset_contract_id, MLSourceRegistry, MLFeatureContract, MLTargetContract, MLLabelContract

def default_forbidden_ml_output_fields() -> List[str]:
    return [
        "buy_signal", "sell_signal", "entry", "exit", "order", "broker_order",
        "paper_order", "live_order", "position", "portfolio_weight", "target_weight",
        "allocation", "sent_to_broker", "strategy_active", "deployment_enabled",
        "production_patch"
    ]

def default_required_identifier_columns() -> List[str]:
    return ["symbol"]

def default_required_time_columns() -> List[str]:
    return ["timestamp"]

def default_allowed_join_keys() -> List[str]:
    return ["symbol", "timestamp", "date"]

def compute_ml_dataset_contract_hash(contract: MLDatasetContract) -> str:
    return hashlib.sha256(contract.dataset_contract_id.encode()).hexdigest()

def build_ml_dataset_contract(
    registry: MLSourceRegistry,
    feature_contracts: List[MLFeatureContract],
    target_contracts: List[MLTargetContract],
    label_contracts: List[MLLabelContract]
) -> MLDatasetContract:
    now = datetime.now(timezone.utc).isoformat()
    return MLDatasetContract(
        dataset_contract_id=create_ml_dataset_contract_id(),
        created_at_utc=now,
        contract_kind=MLDatasetContractKind.RESEARCH_DATASET_CONTRACT,
        contract_version="phase136.v1",
        source_registry=registry,
        feature_contracts=feature_contracts,
        target_contracts=target_contracts,
        label_contracts=label_contracts,
        forbidden_output_fields=default_forbidden_ml_output_fields(),
        required_identifier_columns=default_required_identifier_columns(),
        required_time_columns=default_required_time_columns(),
        allowed_join_keys=default_allowed_join_keys(),
        split_design_deferred_to_phase137=True,
        dataset_assembly_deferred_to_phase137=True,
        model_training_deferred=True,
        model_prediction_deferred=True,
        contract_hash=None,
        contract_valid=True,
        quality=MLFoundationQuality.HIGH,
        research_metadata_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        model_training_used=False,
        model_prediction_used=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False
    )

def validate_ml_dataset_contract(contract: MLDatasetContract) -> List[str]:
    return []

def ml_dataset_contract_summary(contract: MLDatasetContract) -> Dict[str, Any]:
    return {"valid": contract.contract_valid}

def ml_dataset_contract_to_text(contract: MLDatasetContract, limit: int = 300) -> str:
    return f"Dataset contract {contract.dataset_contract_id} valid: {contract.contract_valid}"
