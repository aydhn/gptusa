from typing import Any, Dict, List
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSimulationContext, ShadowSignal, create_shadow_signal_id, get_utc_now_str
)

def generate_shadow_signals(context: ShadowSimulationContext) -> List[ShadowSignal]:
    if context.runtime_mode.value == "MOCK_SHADOW":
        return generate_mock_shadow_signals()
    return []

def generate_mock_shadow_signals(symbols: List[str] | None = None) -> List[ShadowSignal]:
    if not symbols:
        symbols = ["AAPL", "MSFT", "GOOGL"]

    signals = []
    for sym in symbols:
        signals.append(ShadowSignal(
            signal_id=create_shadow_signal_id(sym),
            created_at_utc=get_utc_now_str(),
            symbol=sym,
            strategy_name="MockShadowStrategy",
            signal_family="Trend",
            side="BUY",
            score=75.0,
            confidence=0.8,
            reason="Mock shadow signal for rehearsal."
        ))
    return signals

def validate_shadow_signals_safe(signals: List[ShadowSignal]) -> List[str]:
    errors = []
    for sig in signals:
        if "gerçek" in sig.reason.lower() or "kesin" in sig.reason.lower():
            errors.append(f"Unsafe language in signal reason for {sig.symbol}")
    return errors

def shadow_signal_summary(signals: List[ShadowSignal]) -> Dict[str, Any]:
    return {
        "count": len(signals),
        "buy_count": sum(1 for s in signals if s.side == "BUY"),
        "sell_count": sum(1 for s in signals if s.side == "SELL")
    }

def shadow_signals_to_text(signals: List[ShadowSignal], limit: int = 50) -> str:
    s = shadow_signal_summary(signals)
    return f"ShadowSignals(count={s['count']}, buy={s['buy_count']}, sell={s['sell_count']})"
