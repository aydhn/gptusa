import hashlib
from typing import Any, Dict, List

from usa_signal_bot.core.enums import MarketStateDatasetStatus, MarketStateColumnKind, RegimeFoundationRiskFlag
from usa_signal_bot.regime_classification.foundation.phase126_models import (
    MarketStateColumnContract,
    MarketStateDatasetContract,
    create_market_state_column_contract_id,
    create_market_state_dataset_contract_id,
    _now
)

FORBIDDEN_COLUMNS = [
    "buy_signal", "sell_signal", "entry", "exit", "order", "broker", "position",
    "portfolio_weight", "target_weight", "allocation", "live_order", "demo_order", "sent_to_broker"
]

def build_default_market_state_column_contracts() -> List[MarketStateColumnContract]:
    columns = [
        ("symbol", MarketStateColumnKind.SYMBOL, "str", True),
        ("timestamp", MarketStateColumnKind.TIMESTAMP, "datetime64[ns]", True),
        ("market_index_context", MarketStateColumnKind.MARKET_INDEX_CONTEXT, "float64", True),
        ("volatility_context", MarketStateColumnKind.VOLATILITY_CONTEXT, "float64", True),
        ("trend_context", MarketStateColumnKind.TREND_CONTEXT, "float64", True),
        ("momentum_context", MarketStateColumnKind.MOMENTUM_CONTEXT, "float64", True),
        ("liquidity_context", MarketStateColumnKind.LIQUIDITY_CONTEXT, "float64", True),
        ("breadth_context", MarketStateColumnKind.BREADTH_CONTEXT, "float64", True),
        ("factor_context", MarketStateColumnKind.FACTOR_CONTEXT, "float64", True),
        ("data_quality_context", MarketStateColumnKind.DATA_QUALITY_CONTEXT, "float64", True),
        ("event_context", MarketStateColumnKind.EVENT_CONTEXT, "float64", True),
        ("calendar_context", MarketStateColumnKind.CALENDAR_CONTEXT, "float64", True),
        ("regime_label_placeholder", MarketStateColumnKind.REGIME_LABEL_PLACEHOLDER, "str", True),
        ("regime_confidence_placeholder", MarketStateColumnKind.METADATA, "float64", True),
        ("regime_source_metadata", MarketStateColumnKind.METADATA, "str", True),
    ]

    return [
        MarketStateColumnContract(
            column_id=create_market_state_column_contract_id(),
            created_at_utc=_now(),
            column_name=name,
            column_kind=kind,
            dtype=dtype,
            required=req,
            nullable=not req,
            description=f"Placeholder for {name}",
            source_artifact_kind=None,
            research_metadata_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
        for name, kind, dtype, req in columns
    ]

def validate_market_state_column_contract(column: MarketStateColumnContract) -> List[str]:
    errors = []
    if column.column_name.lower() in FORBIDDEN_COLUMNS:
        errors.append(f"Forbidden column name: {column.column_name}")
    if not column.research_metadata_only:
        errors.append(f"Column {column.column_name} is not marked as research_metadata_only")
    if column.produces_trade_signal or column.produces_order_decision or column.produces_portfolio_weights:
        errors.append(f"Column {column.column_name} is marked as producing execution output")
    return errors

def compute_market_state_schema_hash(contract: MarketStateDatasetContract) -> str:
    schema_str = f"{contract.dataset_name}_{contract.version}_" + "_".join([c.column_name for c in contract.columns])
    return hashlib.sha256(schema_str.encode("utf-8")).hexdigest()

def build_market_state_dataset_contract(version: str = "phase126.v1") -> MarketStateDatasetContract:
    columns = build_default_market_state_column_contracts()

    errors = []
    risk_flags = []
    for col in columns:
        col_errs = validate_market_state_column_contract(col)
        if col_errs:
            errors.extend(col_errs)
            risk_flags.append(RegimeFoundationRiskFlag.FORBIDDEN_REGIME_COLUMN)

    req_cols = [c.column_name for c in columns if c.required]

    contract = MarketStateDatasetContract(
        contract_id=create_market_state_dataset_contract_id(),
        created_at_utc=_now(),
        status=MarketStateDatasetStatus.CREATED if not errors else MarketStateDatasetStatus.BLOCKED,
        dataset_name="market_state_dataset",
        version=version,
        columns=columns,
        required_columns=req_cols,
        optional_columns=[],
        primary_key_columns=["symbol", "timestamp"],
        timestamp_column="timestamp",
        symbol_column="symbol",
        label_placeholder_columns=["regime_label_placeholder"],
        schema_hash=None,
        research_data_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=errors,
        risk_flags=risk_flags,
        metadata={}
    )

    contract.schema_hash = compute_market_state_schema_hash(contract)
    return contract

def validate_market_state_dataset_contract(contract: MarketStateDatasetContract) -> List[str]:
    errors = []
    if not contract.research_data_only:
        errors.append("Dataset contract is not marked as research_data_only")
    if contract.activation_allowed or contract.strategy_activation_allowed:
        errors.append("Dataset contract activation is illegally enabled")
    if contract.produces_trade_signal or contract.produces_order_decision or contract.produces_portfolio_weights:
        errors.append("Dataset contract produces execution outputs")
    for col in contract.columns:
        errors.extend(validate_market_state_column_contract(col))
    return errors

def market_state_dataset_contract_summary(contract: MarketStateDatasetContract) -> dict[str, Any]:
    return {
        "contract_id": contract.contract_id,
        "dataset_name": contract.dataset_name,
        "version": contract.version,
        "column_count": len(contract.columns),
        "status": contract.status.value
    }

def market_state_dataset_contract_to_text(contract: MarketStateDatasetContract, limit: int = 300) -> str:
    lines = [
        f"Dataset Contract ID: {contract.contract_id}",
        f"Name: {contract.dataset_name} (v{contract.version})",
        f"Status: {contract.status.value}",
        f"Columns ({len(contract.columns)}):"
    ]
    for col in contract.columns[:limit]:
        lines.append(f"  - {col.column_name} ({col.dtype})")

    if contract.errors:
        lines.append("Errors:")
        for err in contract.errors:
            lines.append(f"  - {err}")

    return "\n".join(lines)
