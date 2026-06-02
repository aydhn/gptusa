from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.backtesting.phase146_models import (
    ExecutionAssumptionContract,
    create_execution_assumption_contract_id
)
from usa_signal_bot.core.enums import ExecutionAssumptionKind

def build_default_execution_assumption() -> ExecutionAssumptionContract:
    return ExecutionAssumptionContract(
        assumption_id=create_execution_assumption_contract_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        execution_kind=ExecutionAssumptionKind.MARKET_ON_NEXT_OPEN,
        description="Assumes market order execution on the open of the next available bar. Research context only.",
        execution_price_source="NEXT_BAR_OPEN",
        fill_price_policy="OPEN_PRICE_WITH_SLIPPAGE",
        allow_same_bar_execution=False,
        allow_next_bar_execution=True,
        allow_live_execution=False,
        order_creation_allowed=False,
        broker_execution_allowed=False,
        assumption_valid=True,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_execution_assumption(item: ExecutionAssumptionContract) -> list[str]:
    errors = []
    if item.allow_live_execution:
        errors.append("allow_live_execution must be False")
    if item.order_creation_allowed:
        errors.append("order_creation_allowed must be False")
    if item.broker_execution_allowed:
        errors.append("broker_execution_allowed must be False")
    return errors

def execution_assumption_summary(item: ExecutionAssumptionContract) -> dict[str, Any]:
    return {"valid": item.assumption_valid, "kind": item.execution_kind.value}

def execution_assumption_to_text(item: ExecutionAssumptionContract, limit: int = 300) -> str:
    return f"ExecutionAssumption(valid={item.assumption_valid}, live_exec={item.allow_live_execution})"
