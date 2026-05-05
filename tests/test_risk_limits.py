import pytest
from usa_signal_bot.core.enums import SignalAction, RiskCheckStatus, RiskSeverity
from usa_signal_bot.risk.risk_limits import (
    default_risk_limit_config,
    validate_risk_limit_config,
    check_max_position_notional,
    check_max_position_pct_equity,
    check_symbol_exposure,
    check_strategy_exposure,
    check_portfolio_exposure,
    check_open_positions_count,
    check_cash_buffer,
    check_short_allowed
)

def test_default_config_valid():
    cfg = default_risk_limit_config()
    validate_risk_limit_config(cfg)

def test_check_max_position_notional():
    cfg = default_risk_limit_config()
    cfg.max_position_notional = 1000.0
    res = check_max_position_notional(500.0, cfg)
    assert res.status == RiskCheckStatus.PASSED

    res = check_max_position_notional(1500.0, cfg)
    assert res.status == RiskCheckStatus.WARNING

def test_check_max_position_pct_equity():
    cfg = default_risk_limit_config()
    cfg.max_position_pct_equity = 0.1
    res = check_max_position_pct_equity(5000.0, 100000.0, cfg) # 5%
    assert res.status == RiskCheckStatus.PASSED

    res = check_max_position_pct_equity(15000.0, 100000.0, cfg) # 15%
    assert res.status == RiskCheckStatus.WARNING

def test_check_symbol_exposure():
    cfg = default_risk_limit_config()
    cfg.max_symbol_exposure_pct = 0.2
    res = check_symbol_exposure("AAPL", 10000.0, 5000.0, 100000.0, cfg) # 15%
    assert res.status == RiskCheckStatus.PASSED

    res = check_symbol_exposure("AAPL", 16000.0, 5000.0, 100000.0, cfg) # 21%
    assert res.status == RiskCheckStatus.FAILED

def test_check_short_allowed():
    cfg = default_risk_limit_config()
    cfg.allow_short = False

    res = check_short_allowed(SignalAction.LONG, cfg)
    assert res.status == RiskCheckStatus.PASSED

    res = check_short_allowed(SignalAction.SHORT, cfg)
    assert res.status == RiskCheckStatus.FAILED
    assert res.severity == RiskSeverity.CRITICAL

def test_check_cash_buffer():
    cfg = default_risk_limit_config()
    cfg.min_cash_buffer_pct = 0.05 # 5k on 100k

    res = check_cash_buffer(10000.0, 2000.0, 100000.0, cfg) # 8k remaining > 5k
    assert res.status == RiskCheckStatus.PASSED

    res = check_cash_buffer(6000.0, 2000.0, 100000.0, cfg) # 4k remaining < 5k
    assert res.status == RiskCheckStatus.FAILED
