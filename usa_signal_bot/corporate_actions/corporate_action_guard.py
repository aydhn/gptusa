from usa_signal_bot.corporate_actions.corporate_action_models import AdjustedPriceValidationResult
"""Corporate Action Guard."""
from typing import Any
from datetime import datetime, timezone

from usa_signal_bot.core.enums import CorporateActionGuardStatus, CorporateActionSeverity, AdjustedPriceValidationStatus
from usa_signal_bot.corporate_actions.corporate_action_models import (
    CorporateActionEvent,
    CorporateActionGuardResult,
    create_corporate_action_guard_id
)
from usa_signal_bot.corporate_actions.adjusted_price_validator import validate_adjusted_close_consistency
from usa_signal_bot.corporate_actions.split_detector import detect_possible_splits, split_candidates_to_events
from usa_signal_bot.corporate_actions.dividend_detector import detect_possible_dividend_adjustments, dividend_candidates_to_events
from usa_signal_bot.corporate_actions.gap_anomaly_detector import detect_price_gap_anomalies, detect_volume_anomalies, detect_ohlcv_reset_patterns
from usa_signal_bot.providers.provider_models import ProviderResponse

class CorporateActionGuard:
    def __init__(
        self,
        manual_events: list[CorporateActionEvent] | None = None,
        split_gap_threshold_pct: float = 35.0,
        price_gap_threshold_pct: float = 15.0,
        volume_multiplier_threshold: float = 10.0
    ):
        self.manual_events = manual_events or []
        self.split_gap_threshold_pct = split_gap_threshold_pct
        self.price_gap_threshold_pct = price_gap_threshold_pct
        self.volume_multiplier_threshold = volume_multiplier_threshold

    def evaluate_symbol_rows(self, symbol: str, rows: list[dict[str, Any]], provider_response: ProviderResponse | None = None) -> CorporateActionGuardResult:
        created_at = datetime.now(timezone.utc).isoformat()

        # 1. Collect known events
        symbol_events = [e for e in self.manual_events if e.symbol == symbol]
        # Potentially extract from provider_response metadata here if configured

        # 2. Adjusted price validation
        adj_result = validate_adjusted_close_consistency(symbol, rows)

        # 3. Detect splits and dividends
        split_candidates = detect_possible_splits(symbol, rows, symbol_events)
        div_candidates = detect_possible_dividend_adjustments(symbol, rows, symbol_events)

        # 4. Detect anomalies
        price_anomalies = detect_price_gap_anomalies(symbol, rows, self.price_gap_threshold_pct)
        vol_anomalies = detect_volume_anomalies(symbol, rows, self.volume_multiplier_threshold)
        reset_anomalies = detect_ohlcv_reset_patterns(symbol, rows)

        all_anomalies = price_anomalies + vol_anomalies + reset_anomalies

        # Combine inferred events if confidence is high enough
        inferred_events = []
        for c in split_candidates:
            if c["confidence"] >= 0.7 and not c["known_event_match"]:
                inferred_events.extend(split_candidates_to_events(symbol, [c]))

        all_events = symbol_events + inferred_events

        status, severity = self.decide_guard_status(all_events, adj_result, split_candidates, all_anomalies)

        result = CorporateActionGuardResult(
            guard_id=create_corporate_action_guard_id(symbol),
            symbol=symbol,
            created_at_utc=created_at,
            status=status,
            severity=severity,
            events=all_events,
            adjusted_validation=adj_result,
            detected_splits=split_candidates,
            detected_dividends=div_candidates,
            gap_anomalies=all_anomalies,
            recommended_guards=[]
        )

        result.recommended_guards = self.recommended_guards_for_result(result)
        return result

    def evaluate_provider_response(self, response: ProviderResponse) -> list[CorporateActionGuardResult]:
        results = []
        for symbol, rows in response.data.items():
            if rows:
                results.append(self.evaluate_symbol_rows(symbol, rows, response))
        return results

    def decide_guard_status(
        self,
        events: list[CorporateActionEvent],
        adjusted_result: AdjustedPriceValidationResult | None,
        split_candidates: list[dict[str, Any]],
        gap_anomalies: list[dict[str, Any]]
    ) -> tuple[CorporateActionGuardStatus, CorporateActionSeverity]:

        status = CorporateActionGuardStatus.CLEAR
        severity = CorporateActionSeverity.NONE

        if events:
            status = CorporateActionGuardStatus.WATCH
            severity = CorporateActionSeverity.LOW

        if gap_anomalies or split_candidates:
            status = CorporateActionGuardStatus.WARNING
            severity = CorporateActionSeverity.MODERATE

        # Check severe conditions
        if adjusted_result and adjusted_result.status == AdjustedPriceValidationStatus.INCONSISTENT:
            status = CorporateActionGuardStatus.REVIEW_REQUIRED
            severity = CorporateActionSeverity.HIGH

        for c in split_candidates:
            if c["confidence"] >= 0.8:
                status = CorporateActionGuardStatus.BLOCK_SIGNAL
                severity = CorporateActionSeverity.HIGH
                break

        for a in gap_anomalies:
            if a["type"] == "PRICE_GAP" and a.get("diff_pct", 0) > self.split_gap_threshold_pct:
                status = CorporateActionGuardStatus.REVIEW_REQUIRED
                severity = CorporateActionSeverity.CRITICAL
                break

        return status, severity

    def recommended_guards_for_result(self, result: CorporateActionGuardResult) -> list[str]:
        guards = []

        if result.status in [CorporateActionGuardStatus.BLOCK_SIGNAL, CorporateActionGuardStatus.REVIEW_REQUIRED]:
            guards.append("block_signal_if_adjusted_inconsistent")
            guards.append("require_manual_review")

        if result.detected_splits or any(e.action_type.value == "SPLIT" for e in result.events):
            guards.append("skip_n_days_after_split")
            guards.append("recompute_indicators_after_adjustment")

        if result.status == CorporateActionGuardStatus.WARNING:
            guards.append("mark_candidate_lower_confidence")

        if result.events:
            guards.append("skip_signal_on_action_date")
            guards.append("use_adjusted_prices_for_backtest")

        return list(set(guards))
