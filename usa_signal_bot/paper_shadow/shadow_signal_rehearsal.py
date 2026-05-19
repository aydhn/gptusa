from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSignal,
    ShadowSimulationContext,
    create_shadow_signal_id
)

def generate_shadow_signals(context: ShadowSimulationContext) -> list[ShadowSignal]:
    return generate_mock_shadow_signals()

def generate_mock_shadow_signals(symbols: list[str] | None = None) -> list[ShadowSignal]:
    if not symbols:
        symbols = ["AAPL", "MSFT"]
    signals = []
    for sym in symbols:
        signals.append(ShadowSignal(
            signal_id=create_shadow_signal_id(sym),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            symbol=sym,
            side="BUY",
            reason="Mock shadow signal",
            score=80.0,
            confidence=0.9
        ))
    return signals

def validate_shadow_signals_safe(signals: list[ShadowSignal]) -> list[str]:
    errors = []
    for sig in signals:
        reason = sig.reason.lower()
        if "kesin al" in reason or "garanti" in reason:
            errors.append(f"Unsafe language in signal reason for {sig.symbol}")
    return errors

def shadow_signal_summary(signals: list[ShadowSignal]) -> dict[str, Any]:
    return {
        "count": len(signals),
        "symbols": [s.symbol for s in signals]
    }

def shadow_signals_to_text(signals: list[ShadowSignal], limit: int = 50) -> str:
    summary = shadow_signal_summary(signals)
    text = f"Shadow Signals (Count: {summary['count']})\n"
    for sig in signals[:limit]:
        text += f"- {sig.symbol} {sig.side} (Score: {sig.score})\n"
    return text
