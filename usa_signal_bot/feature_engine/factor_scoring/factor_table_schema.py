from typing import Any
import pandas as pd
from datetime import datetime, timezone

from usa_signal_bot.feature_engine.factor_scoring.phase121_models import (
    FactorTableSchema,
    FactorOutputKind,
    FactorBlockedOutputKind,
    create_factor_table_schema_id
)

def allowed_factor_output_kinds() -> list[FactorOutputKind]:
    return [
        FactorOutputKind.FACTOR_RAW_SCORE,
        FactorOutputKind.FACTOR_NORMALIZED_SCORE,
        FactorOutputKind.FACTOR_PERCENTILE,
        FactorOutputKind.FACTOR_RANK,
        FactorOutputKind.FACTOR_DIAGNOSTIC,
        FactorOutputKind.FACTOR_TABLE_METADATA
    ]

def blocked_factor_output_kinds() -> list[FactorBlockedOutputKind]:
    return [
        FactorBlockedOutputKind.TRADE_SIGNAL,
        FactorBlockedOutputKind.ORDER_DECISION,
        FactorBlockedOutputKind.BROKER_INSTRUCTION,
        FactorBlockedOutputKind.PAPER_STATE_MUTATION,
        FactorBlockedOutputKind.PORTFOLIO_WEIGHT,
        FactorBlockedOutputKind.TARGET_WEIGHT,
        FactorBlockedOutputKind.ALLOCATION,
        FactorBlockedOutputKind.LIVE_ORDER,
        FactorBlockedOutputKind.DEMO_ORDER,
        FactorBlockedOutputKind.TELEGRAM_REAL_SEND,
        FactorBlockedOutputKind.DASHBOARD_PAYLOAD,
        FactorBlockedOutputKind.SCRAPED_HTML,
        FactorBlockedOutputKind.PAID_API_PAYLOAD
    ]

def validate_no_forbidden_factor_columns(columns: list[str]) -> list[str]:
    errors = []
    forbidden_fragments = [
        "buy", "sell", "entry", "exit", "order", "broker", "position",
        "portfolio_weight", "target_weight", "allocation", "paper",
        "live", "demo_order", "live_order", "sent_to_broker"
    ]

    for col in columns:
        col_lower = col.lower()
        if "macd_signal" in col_lower:
            continue
        if "signal" in col_lower:
             errors.append(f"Forbidden column contains 'signal': {col}")
        for frag in forbidden_fragments:
            if frag in col_lower:
                errors.append(f"Forbidden column contains '{frag}': {col}")

    return errors

def validate_factor_column_names(columns: list[str]) -> list[str]:
    return validate_no_forbidden_factor_columns(columns)

def build_factor_table_schema(df: pd.DataFrame) -> FactorTableSchema:
    cols = list(df.columns)
    errs = validate_no_forbidden_factor_columns(cols)

    schema = FactorTableSchema(
        schema_id=create_factor_table_schema_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        required_base_columns=["symbol", "timestamp"] if "symbol" in cols and "timestamp" in cols else [],
        factor_columns=[c for c in cols if c not in ["symbol", "timestamp"]],
        allowed_output_kinds=allowed_factor_output_kinds(),
        blocked_output_kinds=blocked_factor_output_kinds(),
        symbol_column="symbol" if "symbol" in cols else "",
        timestamp_column="timestamp" if "timestamp" in cols else "",
        schema_valid=len(errs) == 0,
        trade_signal_columns_present=False,
        order_decision_columns_present=False,
        portfolio_weight_columns_present=False,
        broker_columns_present=False,
        paper_mutation_columns_present=False,
        warnings=[],
        errors=errs,
        risk_flags=[],
        metadata={}
    )
    return schema

def validate_factor_table_schema(schema: FactorTableSchema) -> list[str]:
    if not schema.schema_valid:
        return schema.errors
    return []

def factor_table_schema_summary(schema: FactorTableSchema) -> dict[str, Any]:
    return {"status": "ok"}

def factor_table_schema_to_text(schema: FactorTableSchema) -> str:
    return f"Schema Valid: {schema.schema_valid}"
