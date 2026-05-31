from typing import Any, Dict, List
from datetime import datetime, timezone
from .phase136_models import MLLabelContract, MLLabelKind, create_ml_label_contract_id

def build_regime_context_label_contract() -> MLLabelContract:
    now = datetime.now(timezone.utc).isoformat()
    return MLLabelContract(
        contract_id=create_ml_label_contract_id(),
        created_at_utc=now,
        label_name="regime_context_research_label",
        label_kind=MLLabelKind.REGIME_CONTEXT_LABEL,
        source_column=None,
        label_description="Regime context label",
        class_values=["bull", "bear", "sideways"],
        trade_signal_semantics_allowed=False,
        order_semantics_allowed=False,
        portfolio_semantics_allowed=False,
        leakage_sensitive=True,
        allowed_for_phase137_dataset_assembly=True,
        research_metadata_only=True,
        investment_advice=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    )

def build_research_bucket_label_contract(name: str, class_values: List[str]) -> MLLabelContract:
    now = datetime.now(timezone.utc).isoformat()
    return MLLabelContract(
        contract_id=create_ml_label_contract_id(),
        created_at_utc=now,
        label_name=name,
        label_kind=MLLabelKind.RESEARCH_BUCKET_LABEL,
        source_column=None,
        label_description=f"Bucket label for {name}",
        class_values=class_values,
        trade_signal_semantics_allowed=False,
        order_semantics_allowed=False,
        portfolio_semantics_allowed=False,
        leakage_sensitive=True,
        allowed_for_phase137_dataset_assembly=True,
        research_metadata_only=True,
        investment_advice=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    )

def build_default_ml_label_contracts() -> List[MLLabelContract]:
    return [
        build_regime_context_label_contract(),
        build_research_bucket_label_contract("forward_return_bucket_research_label", ["negative_return_bucket", "neutral_return_bucket", "positive_return_bucket"]),
        build_research_bucket_label_contract("volatility_bucket_research_label", ["low_volatility_bucket", "medium_volatility_bucket", "high_volatility_bucket"]),
        build_research_bucket_label_contract("drawdown_bucket_research_label", ["shallow_drawdown_bucket", "medium_drawdown_bucket", "deep_drawdown_bucket"])
    ]

def validate_ml_label_contracts(items: List[MLLabelContract]) -> List[str]:
    return []

def ml_label_contracts_summary(items: List[MLLabelContract]) -> Dict[str, Any]:
    return {"count": len(items)}

def ml_label_contracts_to_text(items: List[MLLabelContract], limit: int = 300) -> str:
    return f"{len(items)} label contracts"
