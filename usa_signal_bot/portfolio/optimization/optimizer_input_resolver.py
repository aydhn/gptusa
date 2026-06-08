import pandas as pd
from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerInputReference, OptimizerInputKind

FORBIDDEN_COLUMNS = {
    "broker_order", "paper_order", "live_order", "sent_to_broker", "strategy_active",
    "deployment_enabled", "portfolio_weight", "target_weight", "actual_target_weight",
    "actual_portfolio_weight", "allocation", "actual_allocation", "capital_allocation",
    "actual_position_size", "position_size", "order_size", "real_order", "live_signal",
    "buy_signal", "sell_signal", "recommended_weight", "production_patch"
}

ALLOWED_CANDIDATE_COLUMNS = {
    "symbol", "concentration_group", "sandbox_score", "risk_budget_score",
    "robustness_score", "liquidity_score", "cost_score", "previous_sandbox_weight"
}

def build_optimizer_input_references(payloads: Dict[str, Any], dataframes: Optional[Dict[str, pd.DataFrame]] = None) -> List[OptimizerInputReference]:
    refs = []
    if dataframes:
        for k, df in dataframes.items():
            ref = OptimizerInputReference(input_kind=OptimizerInputKind.OPTIMIZER_CANDIDATE_INPUTS, source_artifact_name=k)
            ref.columns = list(df.columns)
            ref.row_count = len(df)
            ref.forbidden_columns_detected = detect_forbidden_optimizer_columns(ref.columns)
            if ref.forbidden_columns_detected:
                ref.errors.append(f"Forbidden columns found: {ref.forbidden_columns_detected}")
            else:
                ref.available = True
            refs.append(ref)

    for k, p in payloads.items():
        ref = OptimizerInputReference(input_kind=OptimizerInputKind.UNKNOWN, source_artifact_name=k)
        fb = detect_forbidden_optimizer_fields(p)
        ref.forbidden_columns_detected = fb
        if fb:
            ref.errors.append(f"Forbidden fields found: {fb}")
        else:
            ref.available = True
        refs.append(ref)

    return refs

def validate_optimizer_candidate_inputs_frame(df: pd.DataFrame) -> List[str]:
    return detect_forbidden_optimizer_columns(list(df.columns))

def detect_forbidden_optimizer_columns(columns: List[str]) -> List[str]:
    return [c for c in columns if c in FORBIDDEN_COLUMNS]

def detect_forbidden_optimizer_fields(payload: Dict[str, Any]) -> List[str]:
    return detect_forbidden_optimizer_columns(list(payload.keys()))

def optimizer_input_resolver_summary(items: List[OptimizerInputReference]) -> Dict[str, Any]:
    return {"count": len(items), "available": sum(1 for i in items if i.available)}

def optimizer_input_resolver_to_text(items: List[OptimizerInputReference], limit: int = 300) -> str:
    return str([i.to_dict() for i in items])[:limit]
