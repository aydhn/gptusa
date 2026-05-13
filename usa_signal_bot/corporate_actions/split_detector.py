"""Split detection heuristic."""
from typing import Any
from usa_signal_bot.core.enums import CorporateActionType, CorporateActionSource
from usa_signal_bot.corporate_actions.corporate_action_models import CorporateActionEvent, create_corporate_action_event_id

def detect_possible_splits(symbol: str, rows: list[dict[str, Any]], known_events: list[CorporateActionEvent] | None = None) -> list[dict[str, Any]]:
    candidates = []

    if len(rows) < 2:
        return candidates

    for i in range(1, len(rows)):
        prev = rows[i-1]
        curr = rows[i]

        prev_close = prev.get("close")
        curr_open = curr.get("open")

        if prev_close and curr_open and prev_close > 0:
            ratio = detect_split_ratio_from_price_gap(prev_close, curr_open)
            if ratio is not None:
                # Calculate volume ratio if possible
                prev_vol = prev.get("volume")
                curr_vol = curr.get("volume")
                vol_change = None
                if prev_vol and curr_vol and prev_vol > 0:
                    vol_change = curr_vol / prev_vol

                conf = classify_split_confidence(ratio, vol_change)

                # Check against known events
                known_match = False
                if known_events:
                    for ke in known_events:
                        if ke.action_type == CorporateActionType.SPLIT and ke.ex_date == curr.get("date", "")[:10]:
                            known_match = True
                            conf = min(1.0, conf + 0.3)

                candidates.append({
                    "date": curr.get("date", "")[:10],
                    "prev_close": prev_close,
                    "curr_open": curr_open,
                    "inferred_ratio": ratio,
                    "volume_change": vol_change,
                    "confidence": conf,
                    "known_event_match": known_match
                })

    return candidates

def detect_split_ratio_from_price_gap(prev_close: float, current_open: float) -> float | None:
    # Heuristic: looking for near integer ratios like 2, 3, 4, 5, 10 or 0.5, 0.33, 0.25
    ratio = prev_close / current_open

    # We allow some tolerance (e.g., 5%) because open price might gap naturally besides the split
    tolerance = 0.05

    common_ratios = [2.0, 3.0, 4.0, 5.0, 7.0, 10.0, 20.0, 0.5, 1/3, 0.25, 0.2, 0.1, 0.05]

    for cr in common_ratios:
        if abs(ratio - cr) / cr < tolerance:
            return cr

    return None

def classify_split_confidence(ratio: float | None, volume_change: float | None = None) -> float:
    if ratio is None:
        return 0.0

    conf = 0.4 # base confidence for a matching ratio

    # Ratios that are exact integers are more likely splits
    # Also if volume changes inversely to price ratio

    if volume_change is not None:
        # If ratio is 2 (price halved), volume should ideally double (volume_change ~ 2)
        expected_vol_change = ratio
        if expected_vol_change > 0:
            if abs(volume_change - expected_vol_change) / expected_vol_change < 0.5:
                conf += 0.3

    return min(1.0, conf)

def split_candidates_to_events(symbol: str, candidates: list[dict[str, Any]]) -> list[CorporateActionEvent]:
    events = []
    for c in candidates:
        ratio = c["inferred_ratio"]
        num, den = None, None
        if ratio > 1:
            num = round(ratio)
            den = 1
        else:
            num = 1
            den = round(1/ratio) if ratio > 0 else 1

        events.append(CorporateActionEvent(
            event_id=create_corporate_action_event_id(symbol, CorporateActionType.SPLIT, c["date"]),
            symbol=symbol,
            action_type=CorporateActionType.SPLIT,
            ex_date=c["date"],
            value=None,
            ratio_numerator=num,
            ratio_denominator=den,
            source=CorporateActionSource.INFERRED_FROM_PRICE,
            confidence=c["confidence"],
            notes=[f"Inferred from price gap: {c['prev_close']} -> {c['curr_open']}"]
        ))
    return events

def split_detection_to_text(candidates: list[dict[str, Any]]) -> str:
    lines = [f"Possible Split Candidates ({len(candidates)}):"]
    for c in candidates:
        match_str = " (Matches known event)" if c["known_event_match"] else ""
        lines.append(f"  {c['date']}: Ratio ~{c['inferred_ratio']:.2f}, Conf: {c['confidence']:.2f}{match_str}")
    if not candidates:
        lines.append("  None detected.")
    return "\n".join(lines)
