import pandas as pd
from typing import Any, Dict, List, Optional
import datetime

from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import (
    BenchmarkInputReference,
    BenchmarkInputKind,
    create_benchmark_input_reference_id,
    BenchmarkComparisonRiskFlag
)

def detect_forbidden_benchmark_columns(columns: List[str]) -> List[str]:
    forbidden = {
        "broker_order", "paper_order", "live_order", "sent_to_broker",
        "strategy_active", "deployment_enabled", "portfolio_weight",
        "target_weight", "allocation", "real_order", "live_signal",
        "recommended_weight"
    }
    return [col for col in columns if col in forbidden]

def validate_strategy_equity_curve_frame(df: pd.DataFrame) -> List[str]:
    errors = []
    required_cols = {"timestamp", "simulated_equity"}
    if not required_cols.issubset(df.columns):
        errors.append(f"Missing required equity curve columns. Expected: {required_cols}")
    forbidden = detect_forbidden_benchmark_columns(df.columns.tolist())
    if forbidden:
        errors.append(f"Forbidden columns found: {forbidden}")
    return errors

def validate_strategy_return_series_frame(df: pd.DataFrame) -> List[str]:
    errors = []
    required_cols = {"timestamp", "simple_return", "cumulative_return"}
    if not required_cols.issubset(df.columns):
        errors.append(f"Missing required return series columns. Expected: {required_cols}")
    forbidden = detect_forbidden_benchmark_columns(df.columns.tolist())
    if forbidden:
        errors.append(f"Forbidden columns found: {forbidden}")
    return errors

def validate_price_bars_frame(df: pd.DataFrame) -> List[str]:
    errors = []
    required_cols = {"symbol", "timestamp", "close"}
    if not required_cols.issubset(df.columns):
        errors.append(f"Missing required price bars columns. Expected: {required_cols}")
    forbidden = detect_forbidden_benchmark_columns(df.columns.tolist())
    if forbidden:
        errors.append(f"Forbidden columns found: {forbidden}")
    return errors

def build_benchmark_input_references(
    payloads: Dict[str, Any],
    dataframes: Optional[Dict[str, pd.DataFrame]] = None
) -> List[BenchmarkInputReference]:
    references = []
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    dataframes = dataframes or {}

    for key, payload in payloads.items():
        kind = BenchmarkInputKind.UNKNOWN
        if "equity" in key.lower(): kind = BenchmarkInputKind.STRATEGY_EQUITY_CURVE
        elif "return" in key.lower(): kind = BenchmarkInputKind.STRATEGY_RETURN_SERIES
        elif "price" in key.lower(): kind = BenchmarkInputKind.PRICE_BAR_DATA
        elif "reference" in key.lower(): kind = BenchmarkInputKind.BENCHMARK_REFERENCE_PRICE_DATA

        df = dataframes.get(key)
        errors = []
        forbidden = []
        row_count = None
        cols = []

        if df is not None:
            row_count = len(df)
            cols = df.columns.tolist()
            forbidden = detect_forbidden_benchmark_columns(cols)

            if kind == BenchmarkInputKind.STRATEGY_EQUITY_CURVE:
                errors.extend(validate_strategy_equity_curve_frame(df))
            elif kind == BenchmarkInputKind.STRATEGY_RETURN_SERIES:
                errors.extend(validate_strategy_return_series_frame(df))
            elif kind in (BenchmarkInputKind.PRICE_BAR_DATA, BenchmarkInputKind.BENCHMARK_REFERENCE_PRICE_DATA):
                errors.extend(validate_price_bars_frame(df))

        flags = []
        if forbidden:
            flags.append(BenchmarkComparisonRiskFlag.FORBIDDEN_BENCHMARK_COLUMN)
            errors.append(f"Forbidden execution columns found: {forbidden}")

        ref = BenchmarkInputReference(
            input_ref_id=create_benchmark_input_reference_id(),
            created_at_utc=now_utc,
            input_kind=kind,
            source_artifact_name=key,
            source_path=None,
            source_hash=None,
            available=True,
            read_only=True,
            row_count=row_count,
            columns=cols,
            forbidden_columns_detected=forbidden,
            errors=errors,
            risk_flags=flags
        )
        references.append(ref)
    return references

def benchmark_input_resolver_to_text(items: List[BenchmarkInputReference], limit: int = 300) -> str:
    return f"Resolved {len(items)} inputs"
