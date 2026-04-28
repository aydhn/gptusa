import pytest
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.universe.models import UniverseSymbol
from usa_signal_bot.strategies.models import Signal, SignalBatch
from usa_signal_bot.paper.models import PaperOrder
from usa_signal_bot.portfolio.models import Position, PortfolioSnapshot
from usa_signal_bot.risk.models import RiskLimits
from usa_signal_bot.regimes.models import RegimeState
from usa_signal_bot.ml.models import Prediction
from usa_signal_bot.backtesting.models import BacktestResult
from usa_signal_bot.core.exceptions import DataValidationError
from usa_signal_bot.core.enums import AssetType, SignalSide, PositionSide

def test_ohlcv_bar_valid():
    bar = OHLCVBar(symbol="AAPL", timestamp_utc="2023-01-01T00:00:00Z", open=150, high=155, low=149, close=152, volume=1000)
    assert bar.symbol == "AAPL"

def test_ohlcv_bar_invalid():
    with pytest.raises(DataValidationError):
        OHLCVBar(symbol="AAPL", timestamp_utc="2023-01-01T00:00:00Z", open=150, high=149, low=155, close=152, volume=1000)

def test_universe_symbol_valid():
    sym = UniverseSymbol(symbol="SPY", asset_type=AssetType.ETF)
    assert sym.symbol == "SPY"

def test_signal_invalid_confidence():
    with pytest.raises(DataValidationError):
        Signal(symbol="AAPL", strategy_name="Test", confidence=1.5)

def test_signal_batch_top_signals():
    s1 = Signal(symbol="A", strategy_name="T", score=10)
    s2 = Signal(symbol="B", strategy_name="T", score=90)
    s3 = Signal(symbol="C", strategy_name="T", score=50)
    batch = SignalBatch(signals=[s1, s2, s3])
    top = batch.top_signals(2)
    assert len(top) == 2
    assert top[0].symbol == "B"
    assert top[1].symbol == "C"

def test_paper_order_invalid_quantity():
    with pytest.raises(DataValidationError):
        PaperOrder(symbol="AAPL", quantity=-10)

def test_portfolio_exposure():
    p1 = Position(symbol="AAPL", side=PositionSide.LONG, quantity=10, average_price=100, market_price=150)
    p2 = Position(symbol="TSLA", side=PositionSide.SHORT, quantity=5, average_price=200, market_price=250)
    snap = PortfolioSnapshot(positions=[p1, p2])

    assert snap.open_position_count() == 2
    # Gross: |10*150| + |-5*250| = 1500 + 1250 = 2750
    assert snap.gross_exposure() == 2750
    # Net: 10*150 - 5*250 = 1500 - 1250 = 250
    assert snap.net_exposure() == 250

def test_risk_limits_invalid_ratio():
    with pytest.raises(DataValidationError):
        RiskLimits(max_position_pct=1.5)

def test_regime_state_invalid_confidence():
    with pytest.raises(DataValidationError):
        RegimeState(confidence=1.1)

def test_models_are_serializable():
    # Just testing that dataclass_to_dict doesn't blow up on complex objects
    from usa_signal_bot.core.serialization import dataclass_to_dict
    res = BacktestResult()
    pred = Prediction()
    assert isinstance(dataclass_to_dict(res), dict)
    assert isinstance(dataclass_to_dict(pred), dict)
