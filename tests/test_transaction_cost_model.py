import pytest
from usa_signal_bot.backtesting.transaction_cost_model import build_flat_bps_transaction_cost_model

def test_transaction_cost_model():
    m = build_flat_bps_transaction_cost_model(1.0)
    assert m.flat_bps == 1.0
    assert m.live_broker_fee_sync_enabled is False
