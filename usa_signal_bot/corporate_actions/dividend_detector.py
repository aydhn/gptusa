"""Dividend detection heuristic."""
from typing import Any
from usa_signal_bot.core.enums import CorporateActionType, CorporateActionSource
from usa_signal_bot.corporate_actions.corporate_action_models import CorporateActionEvent, create_corporate_action_event_id

def detect_possible_dividend_adjustments(symbol: str, rows: list[dict[str, Any]], known_events: list[CorporateActionEvent] | None = None) -> list[dict[str, Any]]:
    candidates = []

    if len(rows) < 2:
        return candidates

    for i in range(1, len(rows)):
        prev = rows[i-1]
        curr = rows[i]

        prev_close = prev.get("close")
        curr_open = curr.get("open")

        if prev_close and curr_open and prev_close > 0:
            div = estimate_dividend_gap(prev_close, curr_open)
            if div is not None:

                # Look for known event
                known_match = False
                conf = 0.3
                if known_events:
                    for ke in known_events:
                        if ke.action_type == CorporateActionType.DIVIDEND and ke.ex_date == curr.get("date", "")[:10]:
                            known_match = True
                            conf = 0.9

                candidates.append({
                    "date": curr.get("date", "")[:10],
                    "prev_close": prev_close,
                    "curr_open": curr_open,
                    "estimated_dividend": div,
                    "confidence": conf,
                    "known_event_match": known_match
                })

    return candidates

def estimate_dividend_gap(prev_close: float, current_open: float, threshold_pct: float = 1.0) -> float | None:
    # A simple heuristic: if open is lower than prev close by a small margin, it MIGHT be a dividend
    # Note: Market gaps down naturally all the time, so confidence is very low without known event.
    drop = prev_close - current_open
    if drop > 0:
        drop_pct = drop / prev_close * 100
        if 0.5 <= drop_pct <= 10.0: # Arbitrary range for typical dividends vs special dividends
            return drop
    return None

def dividend_candidates_to_events(symbol: str, candidates: list[dict[str, Any]]) -> list[CorporateActionEvent]:
    events = []
    for c in candidates:
        events.append(CorporateActionEvent(
            event_id=create_corporate_action_event_id(symbol, CorporateActionType.DIVIDEND, c["date"]),
            symbol=symbol,
            action_type=CorporateActionType.DIVIDEND,
            ex_date=c["date"],
            value=c["estimated_dividend"],
            ratio_numerator=None,
            ratio_denominator=None,
            source=CorporateActionSource.INFERRED_FROM_PRICE,
            confidence=c["confidence"],
            notes=[f"Inferred from price gap: {c['prev_close']} -> {c['curr_open']}"]
        ))
    return events

def dividend_detection_to_text(candidates: list[dict[str, Any]]) -> str:
    lines = [f"Possible Dividend Candidates ({len(candidates)}):"]
    for c in candidates:
        match_str = " (Matches known event)" if c["known_event_match"] else ""
        lines.append(f"  {c['date']}: Drop ~{c['estimated_dividend']:.2f}, Conf: {c['confidence']:.2f}{match_str}")
    if not candidates:
        lines.append("  None detected.")
    return "\n".join(lines)
