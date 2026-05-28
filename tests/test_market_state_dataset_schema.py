from usa_signal_bot.regime_classification.foundation.market_state_dataset_schema import (
    build_market_state_dataset_contract,
    validate_market_state_dataset_contract,
    FORBIDDEN_COLUMNS
)
from usa_signal_bot.regime_classification.foundation.phase126_models import MarketStateColumnContract
from usa_signal_bot.core.enums import MarketStateColumnKind

def test_build_market_state_dataset_contract():
    contract = build_market_state_dataset_contract()
    assert contract.dataset_name == "market_state_dataset"
    assert contract.schema_hash is not None
    assert contract.research_data_only is True
    assert contract.activation_allowed is False
    assert len(contract.errors) == 0

def test_validate_market_state_dataset_contract_with_forbidden():
    contract = build_market_state_dataset_contract()
    contract.columns.append(MarketStateColumnContract(
        column_id="col_123",
        created_at_utc="",
        column_name="buy_signal",
        column_kind=MarketStateColumnKind.METADATA,
        dtype="bool",
        required=False,
        nullable=True,
        description="",
        source_artifact_kind=None,
        research_metadata_only=True,
        produces_trade_signal=True,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    errors = validate_market_state_dataset_contract(contract)
    assert len(errors) > 0
    assert any("Forbidden column name" in str(e) for e in errors)
    assert any("producing execution output" in str(e) for e in errors)
