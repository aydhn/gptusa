from typing import Any, Dict, List
from datetime import datetime, timezone
from .phase136_models import MLTargetContract, MLTargetKind, create_ml_target_contract_id

def build_forward_return_research_target(horizon_bars: int) -> MLTargetContract:
    now = datetime.now(timezone.utc).isoformat()
    return MLTargetContract(
        contract_id=create_ml_target_contract_id(),
        created_at_utc=now,
        target_name=f"forward_return_{horizon_bars}b_research",
        target_kind=MLTargetKind.FORWARD_RETURN_RESEARCH_TARGET,
        horizon_bars=horizon_bars,
        horizon_calendar_days=None,
        source_column=None,
        target_formula_description=f"{horizon_bars}-bar forward return",
        target_directional_language_allowed=False,
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

def build_forward_volatility_research_target(horizon_bars: int) -> MLTargetContract:
    now = datetime.now(timezone.utc).isoformat()
    return MLTargetContract(
        contract_id=create_ml_target_contract_id(),
        created_at_utc=now,
        target_name=f"forward_volatility_{horizon_bars}b_research",
        target_kind=MLTargetKind.FORWARD_VOLATILITY_RESEARCH_TARGET,
        horizon_bars=horizon_bars,
        horizon_calendar_days=None,
        source_column=None,
        target_formula_description=f"{horizon_bars}-bar forward volatility",
        target_directional_language_allowed=False,
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

def build_forward_drawdown_research_target(horizon_bars: int) -> MLTargetContract:
    now = datetime.now(timezone.utc).isoformat()
    return MLTargetContract(
        contract_id=create_ml_target_contract_id(),
        created_at_utc=now,
        target_name=f"forward_drawdown_{horizon_bars}b_research",
        target_kind=MLTargetKind.FORWARD_DRAWDOWN_RESEARCH_TARGET,
        horizon_bars=horizon_bars,
        horizon_calendar_days=None,
        source_column=None,
        target_formula_description=f"{horizon_bars}-bar forward drawdown",
        target_directional_language_allowed=False,
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

def build_default_ml_target_contracts() -> List[MLTargetContract]:
    return [
        build_forward_return_research_target(5),
        build_forward_return_research_target(20),
        build_forward_volatility_research_target(20),
        build_forward_drawdown_research_target(20)
    ]

def validate_ml_target_contracts(items: List[MLTargetContract]) -> List[str]:
    return []

def ml_target_contracts_summary(items: List[MLTargetContract]) -> Dict[str, Any]:
    return {"count": len(items)}

def ml_target_contracts_to_text(items: List[MLTargetContract], limit: int = 300) -> str:
    return f"{len(items)} target contracts"
