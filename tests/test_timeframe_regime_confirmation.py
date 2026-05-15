from usa_signal_bot.regime_map.timeframe_regime_confirmation import MultiTimeframeRegimeConfirmationEngine
from usa_signal_bot.core.enums import RegimeConfirmationStatus

def test_engine_confirmed():
    engine = MultiTimeframeRegimeConfirmationEngine()
    # Steady uptrend
    rows = [{"date": f"2022-{m:02d}-{d:02d}", "open": m*30+d, "high": m*30+d, "low": m*30+d, "close": m*30+d, "volume": 100000}
            for m in range(1, 13) for d in range(1, 28)]

    conf = engine.confirm_symbol("SPY", rows)
    # It should be CONFIRMED or PARTIAL depending on counts, but definitely not conflicted
    assert conf.status in [RegimeConfirmationStatus.CONFIRMED, RegimeConfirmationStatus.PARTIAL]
