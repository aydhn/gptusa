import pandas
from typing import Any
from usa_signal_bot.portfolio.foundation.phase153_models import (
    PortfolioInputReference, PortfolioInputKind, PortfolioFoundationRiskFlag
)

def detect_forbidden_portfolio_columns(columns: list[str]) -> list[str]:
    forbidden = [
        "broker_order", "paper_order", "live_order", "sent_to_broker",
        "strategy_active", "deployment_enabled", "portfolio_weight",
        "target_weight", "allocation", "capital_allocation", "position_size",
        "order_size", "real_order", "live_signal", "buy_signal", "sell_signal",
        "recommended_weight", "production_patch"
    ]
    return [c for c in columns if c in forbidden]

def detect_forbidden_handoff_fields(payload: dict[str, Any]) -> list[str]:
    forbidden = [
        "broker_order", "paper_order", "live_order", "sent_to_broker",
        "strategy_active", "deployment_enabled", "portfolio_weight",
        "target_weight", "allocation", "capital_allocation", "position_size",
        "order_size", "real_order", "live_signal", "buy_signal", "sell_signal",
        "recommended_weight", "production_patch"
    ]
    detected = []
    for k in payload.keys():
        if k in forbidden:
            detected.append(k)
    return detected

def validate_candidate_universe_input_frame(df: pandas.DataFrame) -> list[str]:
    errors = []
    forbidden = detect_forbidden_portfolio_columns(list(df.columns))
    if forbidden:
        errors.append(f"Forbidden columns detected: {forbidden}")
    if "symbol" not in df.columns:
        errors.append("Missing required column: symbol")
    return errors

def build_portfolio_input_references(payloads: dict[str, Any], dataframes: dict[str, pandas.DataFrame] | None = None) -> list[PortfolioInputReference]:
    refs = []

    for name, payload in payloads.items():
        ref = PortfolioInputReference()
        ref.source_artifact_name = name
        ref.available = True
        ref.input_kind = PortfolioInputKind.UNKNOWN

        if "package" in name.lower():
            ref.input_kind = PortfolioInputKind.PHASE153_HANDOFF_PACKAGE
        elif "contract" in name.lower():
            ref.input_kind = PortfolioInputKind.PHASE153_HANDOFF_CONTRACT

        forbidden = detect_forbidden_handoff_fields(payload)
        if forbidden:
            ref.forbidden_columns_detected = forbidden
            ref.errors.append(f"Forbidden fields detected: {forbidden}")
            ref.risk_flags.append(PortfolioFoundationRiskFlag.FORBIDDEN_HANDOFF_FIELD)

        refs.append(ref)

    if dataframes:
        for name, df in dataframes.items():
            ref = PortfolioInputReference()
            ref.source_artifact_name = name
            ref.available = True
            ref.input_kind = PortfolioInputKind.CANDIDATE_UNIVERSE_FILE
            ref.row_count = len(df)
            ref.columns = list(df.columns)

            forbidden = detect_forbidden_portfolio_columns(ref.columns)
            if forbidden:
                ref.forbidden_columns_detected = forbidden
                ref.errors.append(f"Forbidden columns detected: {forbidden}")
                ref.risk_flags.append(PortfolioFoundationRiskFlag.FORBIDDEN_PORTFOLIO_COLUMN)

            refs.append(ref)

    return refs

def portfolio_input_resolver_summary(items: list[PortfolioInputReference]) -> dict[str, Any]:
    return {
        "count": len(items),
        "available_count": sum(1 for item in items if item.available),
        "forbidden_detected": any(item.forbidden_columns_detected for item in items)
    }

def portfolio_input_resolver_to_text(items: list[PortfolioInputReference], limit: int = 300) -> str:
    lines = [f"Resolved Inputs ({len(items)}):"]
    for item in items:
        lines.append(f" - {item.source_artifact_name} ({item.input_kind.value}) | Errors: {len(item.errors)}")
    return "\n".join(lines)
