from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.backtesting.phase146_models import (
    BacktestDatasetContract,
    BacktestInputReference,
    BacktestInputKind,
    create_backtest_dataset_contract_id
)
from usa_signal_bot.core.enums import (
    BacktestDatasetContractStatus,
    BacktestFoundationRiskFlag
)

def build_default_backtest_dataset_contract(inputs: list[BacktestInputReference]) -> BacktestDatasetContract:
    input_kinds = [x.input_kind for x in inputs]

    has_price = BacktestInputKind.PRICE_BAR_DATA in input_kinds

    status = BacktestDatasetContractStatus.VALID if has_price else BacktestDatasetContractStatus.INVALID
    errors = []
    risk_flags = []
    if not has_price:
        errors.append("PRICE_BAR_DATA is missing.")
        risk_flags.append(BacktestFoundationRiskFlag.DATASET_CONTRACT_INVALID)

    contract = BacktestDatasetContract(
        contract_id=create_backtest_dataset_contract_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=status,
        required_inputs=[BacktestInputKind.PRICE_BAR_DATA],
        optional_inputs=[
            BacktestInputKind.ADJUSTED_PRICE_DATA,
            BacktestInputKind.CORPORATE_ACTION_DATA,
            BacktestInputKind.MARKET_CALENDAR_DATA,
            BacktestInputKind.RESEARCH_PREDICTION_OUTPUT
        ],
        required_columns_by_input={
            BacktestInputKind.PRICE_BAR_DATA.value: ["symbol", "timestamp", "open", "high", "low", "close", "volume"]
        },
        time_column="timestamp",
        symbol_column="symbol",
        price_columns=["open", "high", "low", "close"],
        volume_columns=["volume"],
        adjusted_price_required=False,
        corporate_actions_supported=True,
        market_calendar_supported=True,
        min_rows_per_symbol=10,
        timezone_policy="UTC_AWARE",
        survivorship_bias_notice="Dataset may be subject to survivorship bias. Exercise caution.",
        lookahead_bias_notice="Ensure features/predictions use only data available prior to the execution timestamp.",
        contract_valid=(status == BacktestDatasetContractStatus.VALID),
        research_data_only=True,
        offline_backtest_research_only=True,
        warnings=[],
        errors=errors,
        risk_flags=risk_flags,
        metadata={"input_ref_count": len(inputs)}
    )
    return contract

def validate_backtest_dataset_contract(contract: BacktestDatasetContract) -> list[str]:
    errors = []
    if contract.status != BacktestDatasetContractStatus.VALID:
        errors.append("Contract status is not VALID.")
    if not contract.survivorship_bias_notice:
        errors.append("Survivorship bias notice is required.")
    if not contract.lookahead_bias_notice:
        errors.append("Lookahead bias notice is required.")
    if not contract.contract_valid:
        errors.append("contract_valid is False.")
    return errors

def backtest_dataset_contract_summary(contract: BacktestDatasetContract) -> dict[str, Any]:
    return {
        "id": contract.contract_id,
        "status": contract.status.value,
        "valid": contract.contract_valid,
        "errors": len(contract.errors)
    }

def backtest_dataset_contract_to_text(contract: BacktestDatasetContract, limit: int = 300) -> str:
    return f"DatasetContract(status={contract.status.value}, valid={contract.contract_valid})"
