from typing import Any
from usa_signal_bot.paper_shadow.shadow_models import ShadowSignal
from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import validate_shadow_signals_safe

def select_shadow_candidates(signals: list[ShadowSignal], min_score: float = 50.0, max_candidates: int = 10) -> list[ShadowSignal]:
    ranked = rank_shadow_signals(signals)
    filtered = [s for s in ranked if (s.score is None or s.score >= min_score)]
    filtered = filter_shadow_signals_by_safety(filtered)
    return filtered[:max_candidates]

def rank_shadow_signals(signals: list[ShadowSignal]) -> list[ShadowSignal]:
    return sorted(signals, key=lambda s: s.score if s.score is not None else 0.0, reverse=True)

def filter_shadow_signals_by_safety(signals: list[ShadowSignal]) -> list[ShadowSignal]:
    safe_signals = []
    for sig in signals:
        if not validate_shadow_signals_safe([sig]):
            safe_signals.append(sig)
    return safe_signals

def shadow_candidate_summary(candidates: list[ShadowSignal]) -> dict[str, Any]:
    return {
        "count": len(candidates),
        "symbols": [c.symbol for c in candidates]
    }

def shadow_candidates_to_text(candidates: list[ShadowSignal], limit: int = 50) -> str:
    summary = shadow_candidate_summary(candidates)
    text = f"Shadow Candidates (Count: {summary['count']})\n"
    for c in candidates[:limit]:
        text += f"- {c.symbol} {c.side} (Score: {c.score})\n"
    return text
