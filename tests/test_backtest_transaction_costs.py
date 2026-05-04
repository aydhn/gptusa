import pytest
from usa_signal_bot.backtesting.transaction_costs import (
    TransactionCostConfig, TransactionCostModelType, calculate_transaction_cost,
    default_transaction_cost_config, transaction_cost_breakdown_to_dict
)
from usa_signal_bot.core.exceptions import TransactionCostError

def test_default_transaction_cost_config():
    config = default_transaction_cost_config()
    assert config.model_type == TransactionCostModelType.BPS
    assert config.fee_bps == 1.0

def test_none_model():
    config = TransactionCostConfig(model_type=TransactionCostModelType.NONE)
    res = calculate_transaction_cost(10000.0, 100.0, config)
    assert res.total_fee == 0.0

def test_flat_fee_model():
    config = TransactionCostConfig(model_type=TransactionCostModelType.FLAT_FEE, flat_fee=5.0)
    res = calculate_transaction_cost(10000.0, 100.0, config)
    assert res.total_fee == 5.0

def test_bps_model():
    config = TransactionCostConfig(model_type=TransactionCostModelType.BPS, fee_bps=10.0) # 10 bps = 0.1%
    res = calculate_transaction_cost(10000.0, 100.0, config)
    assert res.total_fee == 10.0

def test_per_share_model():
    config = TransactionCostConfig(model_type=TransactionCostModelType.PER_SHARE, per_share_fee=0.01)
    res = calculate_transaction_cost(10000.0, 100.0, config)
    assert res.total_fee == 1.0

def test_combined_model():
    config = TransactionCostConfig(model_type=TransactionCostModelType.COMBINED, flat_fee=1.0, fee_bps=10.0, per_share_fee=0.01)
    res = calculate_transaction_cost(10000.0, 100.0, config)
    assert res.total_fee == 12.0 # 1.0 + 10.0 + 1.0

def test_min_fee():
    config = TransactionCostConfig(model_type=TransactionCostModelType.BPS, fee_bps=1.0, min_fee=5.0)
    res = calculate_transaction_cost(10000.0, 100.0, config) # bps fee is 1.0
    assert res.total_fee == 5.0

def test_max_fee():
    config = TransactionCostConfig(model_type=TransactionCostModelType.BPS, fee_bps=100.0, max_fee=50.0)
    res = calculate_transaction_cost(10000.0, 100.0, config) # bps fee is 100.0
    assert res.total_fee == 50.0

def test_negative_notional():
    config = default_transaction_cost_config()
    with pytest.raises(TransactionCostError):
        calculate_transaction_cost(-100.0, 10.0, config)

def test_breakdown_to_dict():
    config = TransactionCostConfig(model_type=TransactionCostModelType.FLAT_FEE, flat_fee=5.0)
    res = calculate_transaction_cost(10000.0, 100.0, config)
    d = transaction_cost_breakdown_to_dict(res)
    assert d['total_fee'] == 5.0
    assert d['model_type'] == "FLAT_FEE"
