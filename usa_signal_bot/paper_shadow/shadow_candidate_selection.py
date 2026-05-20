from typing import Any, Dict, List
from usa_signal_bot.paper_shadow.shadow_models import ShadowSignal

def select_shadow_candidates(signals: List[ShadowSignal], min_score: float = 50.0, max_candidates: int = 10) -> List[ShadowSignal]:
    safe_signals = filter_shadow_signals_by_safety(signals)
    filtered = [s for s in safe_signals if (s.score or 0.0) >= min_score]
    ranked = rank_shadow_signals(filtered)
    return ranked[:max_candidates]

def rank_shadow_signals(signals: List[ShadowSignal]) -> List[ShadowSignal]:
    return sorted(signals, key=lambda s: s.score or 0.0, reverse=True)

def filter_shadow_signals_by_safety(signals: List[ShadowSignal]) -> List[ShadowSignal]:
    # Placeholder for more complex safety filtering
    return [s for s in signals if "kesin" not in s.reason.lower()]

def shadow_candidate_summary(candidates: List[ShadowSignal]) -> Dict[str, Any]:
    return {
        "count": len(candidates),
        "avg_score": sum(c.score or 0.0 for c in candidates) / len(candidates) if candidates else 0.0
    }

def shadow_candidates_to_text(candidates: List[ShadowSignal], limit: int = 50) -> str:
    s = shadow_candidate_summary(candidates)
    return f"ShadowCandidates(count={s['count']}, avg_score={s['avg_score']:.2f})"
