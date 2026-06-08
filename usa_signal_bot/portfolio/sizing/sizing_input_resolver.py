import pandas as pd
from typing import Any
from usa_signal_bot.portfolio.sizing.phase154_models import SizingInputReference, SizingCandidate, SizingInputKind, SizingPrototypeRiskFlag

FORBIDDEN_SIZING_COLUMNS = [
    "broker_order", "paper_order", "live_order", "sent_to_broker",
    "strategy_active", "deployment_enabled", "portfolio_weight",
    "target_weight", "allocation", "capital_allocation",
    "actual_position_size", "position_size", "order_size",
    "real_order", "live_signal", "buy_signal", "sell_signal",
    "recommended_weight", "production_patch"
]

def build_sizing_input_references(payloads: dict[str, Any], dataframes: dict[str, pd.DataFrame] | None = None) -> list[SizingInputReference]:
    refs = []

    # Process payloads
    for name, payload in payloads.items():
        ref = SizingInputReference(
            source_artifact_name=name,
            available=True
        )
        forbidden = detect_forbidden_sizing_fields(payload)
        ref.forbidden_columns_detected = forbidden
        if forbidden:
            ref.errors.append("Forbidden fields found.")
            ref.risk_flags.append(SizingPrototypeRiskFlag.SIZING_INPUT_INVALID)
        refs.append(ref)

    # Process dataframes
    if dataframes:
        for name, df in dataframes.items():
            ref = SizingInputReference(
                source_artifact_name=name,
                available=True,
                row_count=len(df),
                columns=df.columns.tolist()
            )
            forbidden = detect_forbidden_sizing_columns(ref.columns)
            ref.forbidden_columns_detected = forbidden
            if forbidden:
                ref.errors.append("Forbidden columns found.")
                ref.risk_flags.append(SizingPrototypeRiskFlag.SIZING_INPUT_INVALID)
            refs.append(ref)

    return refs

def build_sizing_candidates(candidate_contract_payload: dict[str, Any], candidate_metrics_df: pd.DataFrame | None = None) -> list[SizingCandidate]:
    candidates = []
    if candidate_metrics_df is not None:
        for _, row in candidate_metrics_df.iterrows():
            cand = SizingCandidate(
                symbol=row.get('symbol', 'UNKNOWN'),
                candidate_valid=True,
                eligible_for_research_prototype=True,
                volatility_proxy=row.get('volatility_proxy'),
                drawdown_proxy=row.get('drawdown_proxy'),
                cost_proxy=row.get('cost_proxy'),
                liquidity_proxy=row.get('liquidity_proxy'),
                robustness_proxy=row.get('robustness_proxy'),
                risk_budget_proxy=row.get('risk_budget_proxy'),
                actual_position_size=None,
                target_weight=None,
                allocation=None,
                order_size=None,
                capital_allocation=None
            )
            candidates.append(cand)
    return candidates

def validate_candidate_metrics_frame(df: pd.DataFrame) -> list[str]:
    errors = []
    forbidden = detect_forbidden_sizing_columns(df.columns.tolist())
    if forbidden:
        errors.append(f"Forbidden columns in candidate metrics: {forbidden}")
    if 'symbol' not in df.columns:
        errors.append("Missing 'symbol' column in candidate metrics.")
    return errors

def validate_risk_budget_inputs_frame(df: pd.DataFrame) -> list[str]:
    errors = []
    forbidden = detect_forbidden_sizing_columns(df.columns.tolist())
    if forbidden:
        errors.append(f"Forbidden columns in risk budget inputs: {forbidden}")
    return errors

def detect_forbidden_sizing_columns(columns: list[str]) -> list[str]:
    return [c for c in columns if c.lower() in FORBIDDEN_SIZING_COLUMNS]

def detect_forbidden_sizing_fields(payload: dict[str, Any]) -> list[str]:
    payload_str = str(payload).lower()
    return [c for c in FORBIDDEN_SIZING_COLUMNS if c.lower() in payload_str]

def sizing_input_resolver_summary(items: list[SizingInputReference]) -> dict[str, Any]:
    return {"ref_count": len(items), "valid": all(not i.errors for i in items)}

def sizing_input_resolver_to_text(items: list[SizingInputReference], limit: int = 300) -> str:
    valid_count = sum(1 for i in items if not i.errors)
    return f"Resolved {len(items)} inputs ({valid_count} valid)"[:limit]
