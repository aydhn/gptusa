from usa_signal_bot.regime_classification.foundation.market_state_dataset_schema import build_market_state_dataset_contract
from usa_signal_bot.regime_classification.foundation.market_state_dataset_skeleton import build_market_state_dataset_skeleton, validate_market_state_dataset_skeleton

def test_build_market_state_dataset_skeleton():
    contract = build_market_state_dataset_contract()
    skeleton = build_market_state_dataset_skeleton(contract, ["SPY"])
    assert skeleton.row_count == 1
    assert skeleton.example_rows[0]["symbol"] == "SPY"
    assert skeleton.example_rows[0]["regime_label_placeholder"] == "unknown_regime"
    assert skeleton.schema_valid is True

def test_validate_market_state_dataset_skeleton():
    contract = build_market_state_dataset_contract()
    skeleton = build_market_state_dataset_skeleton(contract, ["SPY"])
    skeleton.contains_trade_signal = True # Invalid

    errors = validate_market_state_dataset_skeleton(skeleton)
    assert len(errors) == 1
    assert "execution column flags" in errors[0]
