from typing import Any, Dict, List
import datetime

from usa_signal_bot.core.enums import MarketStateDatasetStatus, RegimeFoundationRiskFlag
from usa_signal_bot.regime_classification.foundation.phase126_models import (
    MarketStateDatasetContract,
    MarketStateDatasetSkeleton,
    create_market_state_dataset_skeleton_id,
    _now
)

def build_example_market_state_rows(contract: MarketStateDatasetContract, symbols: List[str]) -> List[dict[str, Any]]:
    rows = []
    base_time = datetime.datetime.now(datetime.timezone.utc)
    for sym in symbols:
        row = {}
        for col in contract.columns:
            if col.column_name == contract.symbol_column:
                row[col.column_name] = sym
            elif col.column_name == contract.timestamp_column:
                row[col.column_name] = base_time.isoformat()
            elif col.column_name in contract.label_placeholder_columns:
                row[col.column_name] = "unknown_regime"
            elif col.dtype == "float64":
                row[col.column_name] = 0.0
            else:
                row[col.column_name] = ""
        rows.append(row)
    return rows

def build_market_state_dataset_skeleton(contract: MarketStateDatasetContract, example_symbols: List[str] | None = None) -> MarketStateDatasetSkeleton:
    if not example_symbols:
        example_symbols = ["SPY", "AAPL", "MSFT"]

    errors = []
    risk_flags = []

    if contract.produces_trade_signal or contract.produces_order_decision or contract.produces_portfolio_weights:
        errors.append("Contract contains execution columns")
        risk_flags.append(RegimeFoundationRiskFlag.MARKET_STATE_DATASET_SCHEMA_INVALID)

    example_rows = build_example_market_state_rows(contract, example_symbols)
    col_names = [c.column_name for c in contract.columns]

    return MarketStateDatasetSkeleton(
        skeleton_id=create_market_state_dataset_skeleton_id(),
        created_at_utc=_now(),
        contract_id=contract.contract_id,
        status=MarketStateDatasetStatus.SKELETON_BUILT if not errors else MarketStateDatasetStatus.BLOCKED,
        columns=col_names,
        example_rows=example_rows,
        row_count=len(example_rows),
        schema_valid=len(errors) == 0,
        research_data_only=True,
        contains_trade_signal=False,
        contains_order_decision=False,
        contains_portfolio_weight=False,
        warnings=[],
        errors=errors,
        risk_flags=risk_flags,
        metadata={}
    )

def validate_market_state_dataset_skeleton(skeleton: MarketStateDatasetSkeleton) -> List[str]:
    errors = []
    if not skeleton.research_data_only:
        errors.append("Skeleton is not marked as research_data_only")
    if skeleton.contains_trade_signal or skeleton.contains_order_decision or skeleton.contains_portfolio_weight:
        errors.append("Skeleton contains execution column flags")
    return errors

def market_state_dataset_skeleton_summary(skeleton: MarketStateDatasetSkeleton) -> dict[str, Any]:
    return {
        "skeleton_id": skeleton.skeleton_id,
        "contract_id": skeleton.contract_id,
        "row_count": skeleton.row_count,
        "schema_valid": skeleton.schema_valid
    }

def market_state_dataset_skeleton_to_text(skeleton: MarketStateDatasetSkeleton, limit: int = 200) -> str:
    lines = [
        f"Skeleton ID: {skeleton.skeleton_id}",
        f"Schema Valid: {skeleton.schema_valid}",
        f"Columns: {len(skeleton.columns)}",
        f"Example Rows: {skeleton.row_count}"
    ]
    if skeleton.errors:
        lines.append("Errors:")
        for err in skeleton.errors:
            lines.append(f"  - {err}")
    return "\n".join(lines)
