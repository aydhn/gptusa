try:
    import pandas as pd
except ImportError:
    pd = None
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import WalkForwardInputKind, WalkForwardRiskFlag
from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    WalkForwardInputReference,
    create_walk_forward_input_reference_id,
    _now_utc
)

FORBIDDEN_COLUMNS = [
    "broker_order",
    "paper_order",
    "live_order",
    "sent_to_broker",
    "strategy_active",
    "deployment_enabled",
    "portfolio_weight",
    "target_weight",
    "allocation",
    "real_order",
    "live_signal",
    "recommended_weight",
    "production_patch"
]

def detect_forbidden_walk_forward_columns(columns: List[str]) -> List[str]:
    return [col for col in columns if col in FORBIDDEN_COLUMNS]

def validate_strategy_return_series_frame(df: Any) -> List[str]:
    errors = []
    if "timestamp" not in df.columns:
        errors.append("Missing 'timestamp' column in strategy return series.")
    if "strategy_return" not in df.columns:
        errors.append("Missing 'strategy_return' column in strategy return series.")
    return errors

def validate_strategy_equity_curve_frame(df: Any) -> List[str]:
    errors = []
    if "timestamp" not in df.columns:
        errors.append("Missing 'timestamp' column in equity curve.")
    if "equity" not in df.columns:
        errors.append("Missing 'equity' column in equity curve.")
    return errors

def validate_price_bars_frame(df: Any) -> List[str]:
    errors = []
    if "timestamp" not in df.columns:
        errors.append("Missing 'timestamp' column in price bars.")
    if "close" not in df.columns:
        errors.append("Missing 'close' column in price bars.")
    return errors

def validate_benchmark_return_series_frame(df: Any) -> List[str]:
    errors = []
    if "timestamp" not in df.columns:
        errors.append("Missing 'timestamp' column in benchmark return series.")
    if "benchmark_return" not in df.columns:
        errors.append("Missing 'benchmark_return' column in benchmark return series.")
    return errors

def build_walk_forward_input_references(
    payloads: Dict[str, Any],
    dataframes: Optional[Dict[str, Any]] = None
) -> List[WalkForwardInputReference]:
    dataframes = dataframes or {}
    refs = []

    mapping = {
        WalkForwardInputKind.STRATEGY_RETURN_SERIES: "strategy_return_series",
        WalkForwardInputKind.STRATEGY_EQUITY_CURVE: "strategy_equity_curve",
        WalkForwardInputKind.PRICE_BAR_DATA: "price_bar_data",
        WalkForwardInputKind.BENCHMARK_RETURN_SERIES: "benchmark_return_series",
        WalkForwardInputKind.BASELINE_COMPARISON_REPORT: "baseline_comparison_report",
        WalkForwardInputKind.RELATIVE_PERFORMANCE_VALIDATION: "relative_performance_validation",
        WalkForwardInputKind.SAFETY_BOUNDARY: "safety_boundary",
        WalkForwardInputKind.PHASE150_READINESS_GATE: "phase150_readiness_gate"
    }

    validators = {
        WalkForwardInputKind.STRATEGY_RETURN_SERIES: validate_strategy_return_series_frame,
        WalkForwardInputKind.STRATEGY_EQUITY_CURVE: validate_strategy_equity_curve_frame,
        WalkForwardInputKind.PRICE_BAR_DATA: validate_price_bars_frame,
        WalkForwardInputKind.BENCHMARK_RETURN_SERIES: validate_benchmark_return_series_frame
    }

    for kind, key in mapping.items():
        payload = payloads.get(key)
        df = dataframes.get(key)

        available = payload is not None or df is not None

        row_count = None
        columns = []
        forbidden = []
        errors = []
        risk_flags = []

        if df is not None:
            row_count = len(df)
            columns = list(df.columns)
            forbidden = detect_forbidden_walk_forward_columns(columns)
            if forbidden:
                errors.append(f"Forbidden columns detected: {forbidden}")
                risk_flags.append(WalkForwardRiskFlag.FORBIDDEN_WALK_FORWARD_COLUMN)

            val_func = validators.get(kind)
            if val_func:
                val_errors = val_func(df)
                errors.extend(val_errors)
                if val_errors:
                    risk_flags.append(WalkForwardRiskFlag.WALK_FORWARD_INPUT_INVALID)
        elif payload is not None and isinstance(payload, dict):
            # Try to get minimal meta
            pass

        if not available:
            errors.append(f"Missing required input: {key}")
            risk_flags.append(WalkForwardRiskFlag.WALK_FORWARD_INPUT_MISSING)

        ref = WalkForwardInputReference(
            input_ref_id=create_walk_forward_input_reference_id(),
            created_at_utc=_now_utc(),
            input_kind=kind,
            source_artifact_name=key,
            source_path=payload.get("source_path") if isinstance(payload, dict) else None,
            source_hash=None,
            available=available,
            read_only=True,
            row_count=row_count,
            columns=columns,
            forbidden_columns_detected=forbidden,
            research_data_only=True,
            offline_backtest_research_only=True,
            errors=errors,
            risk_flags=risk_flags
        )
        refs.append(ref)

    return refs

def walk_forward_input_resolver_summary(items: List[WalkForwardInputReference]) -> Dict[str, Any]:
    available_count = sum(1 for x in items if x.available)
    error_count = sum(len(x.errors) for x in items)
    forbidden_count = sum(len(x.forbidden_columns_detected) for x in items)

    return {
        "total_inputs": len(items),
        "available_inputs": available_count,
        "total_errors": error_count,
        "total_forbidden_columns": forbidden_count,
        "all_available": available_count == len(items),
        "valid": error_count == 0
    }

def walk_forward_input_resolver_to_text(items: List[WalkForwardInputReference], limit: int = 300) -> str:
    summary = walk_forward_input_resolver_summary(items)
    lines = [
        f"WalkForwardInputResolver:",
        f"  Total: {summary['total_inputs']}, Available: {summary['available_inputs']}",
        f"  Valid: {summary['valid']}",
        f"  Errors: {summary['total_errors']}"
    ]
    return "\n".join(lines)[:limit]
