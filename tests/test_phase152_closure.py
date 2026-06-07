import pytest
from usa_signal_bot.backtesting.closure.phase152_models import Phase153ReadinessGate, Phase153ReadinessStatus

def test_phase152_strict_read_only():
    gate = Phase153ReadinessGate()
    assert gate.live_trading_enabled is False
    assert gate.paper_trading_enabled is False
    assert gate.broker_execution_enabled is False
    assert gate.portfolio_construction_executed is False
    assert gate.target_weights_produced is False
    assert gate.deployment_allowed is False
    assert gate.investment_advice is False
