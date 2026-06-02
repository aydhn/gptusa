from typing import Any
from datetime import datetime, timezone
import hashlib
from typing import Any

from usa_signal_bot.backtesting.phase146_models import (
    BacktestInputReference,
    BacktestInputKind,
    create_backtest_input_reference_id
)
from usa_signal_bot.core.enums import BacktestFoundationRiskFlag

FORBIDDEN_ACTIVE_COLUMNS = {
    "buy_signal", "sell_signal", "entry", "exit", "order", "broker_order",
    "paper_order", "live_order", "position", "portfolio_weight",
    "target_weight", "allocation", "sent_to_broker", "strategy_active",
    "deployment_enabled"
}

def detect_forbidden_backtest_columns(columns: list[str]) -> list[str]:
    return [col for col in columns if col.lower() in FORBIDDEN_ACTIVE_COLUMNS]

def validate_price_bars_frame(df: Any) -> list[str]:
    required = ["symbol", "timestamp", "open", "high", "low", "close", "volume"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        return [f"Missing required price bar columns: {missing}"]
    return []

def validate_feature_matrix_frame(df: Any) -> list[str]:
    if "symbol" not in df.columns or "timestamp" not in df.columns:
        return ["Feature matrix must have 'symbol' and 'timestamp' columns"]
    return []

def validate_research_prediction_frame(df: Any) -> list[str]:
    if "symbol" not in df.columns or "timestamp" not in df.columns:
        return ["Research prediction must have 'symbol' and 'timestamp' columns"]
    return []

def build_backtest_input_references(payloads: dict[str, Any], dataframes: dict[str, Any] | None = None) -> list[BacktestInputReference]:
    refs = []
    dataframes = dataframes or {}

    for key, info in payloads.items():
        kind = BacktestInputKind(info.get("kind", BacktestInputKind.UNKNOWN.value))
        df = dataframes.get(key)

        cols = list(df.columns) if df is not None else info.get("columns", [])
        row_count = len(df) if df is not None else info.get("row_count")

        forbidden = detect_forbidden_backtest_columns(cols)
        errors = []
        if df is not None:
            if kind == BacktestInputKind.PRICE_BAR_DATA:
                errors.extend(validate_price_bars_frame(df))
            elif kind == BacktestInputKind.FEATURE_MATRIX:
                errors.extend(validate_feature_matrix_frame(df))
            elif kind == BacktestInputKind.RESEARCH_PREDICTION_OUTPUT:
                errors.extend(validate_research_prediction_frame(df))

        risk_flags = []
        if forbidden:
            errors.append(f"Forbidden columns detected: {forbidden}")
            risk_flags.append(BacktestFoundationRiskFlag.FORBIDDEN_BACKTEST_COLUMN)

        if errors:
            risk_flags.append(BacktestFoundationRiskFlag.INPUT_INVALID)

        ref = BacktestInputReference(
            input_ref_id=create_backtest_input_reference_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            input_kind=kind,
            source_artifact_name=info.get("name", key),
            source_path=info.get("path"),
            source_hash=info.get("hash"),
            available=True,
            read_only=True,
            required=info.get("required", False),
            row_count=row_count,
            columns=cols,
            forbidden_columns_detected=forbidden,
            research_data_only=True,
            offline_backtest_research_only=True,
            warnings=[],
            errors=errors,
            risk_flags=risk_flags,
            metadata={"original_key": key}
        )
        refs.append(ref)
    return refs

def backtest_input_resolver_summary(items: list[BacktestInputReference]) -> dict[str, Any]:
    return {
        "count": len(items),
        "valid_count": sum(1 for x in items if not x.errors),
        "invalid_count": sum(1 for x in items if x.errors),
        "kinds": [x.input_kind.value for x in items]
    }

def backtest_input_resolver_to_text(items: list[BacktestInputReference], limit: int = 300) -> str:
    summary = backtest_input_resolver_summary(items)
    return f"Resolved {summary['count']} inputs. Valid: {summary['valid_count']}"
