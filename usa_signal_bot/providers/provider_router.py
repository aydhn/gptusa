from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    DataProviderName, ProviderResponseStatus, ProviderQualityStatus, ProviderRoutingDecision
)
from usa_signal_bot.providers.provider_models import (
    ProviderRequest, ProviderResponse, ProviderQualityScore, ProviderRoutingResult,
    create_provider_routing_id
)
from usa_signal_bot.providers.provider_interface import BaseDataProvider
from usa_signal_bot.providers.provider_registry import ProviderRegistry
from usa_signal_bot.providers.provider_quality import score_provider_response_quality

from usa_signal_bot.calendar.market_calendar import LocalMarketCalendar

class ProviderRouter:
    def __init__(self, registry, prefer_cache: bool = True, fallback_enabled: bool = True, min_quality_score: float = 60.0, calendar: LocalMarketCalendar | None = None):
        self.registry = registry
        self.prefer_cache = prefer_cache
        self.fallback_enabled = fallback_enabled
        self.min_quality_score = min_quality_score
        self.calendar = calendar

    def try_provider(self, provider, request):
        try:
            response = provider.fetch(request)
        except Exception as e:
            from usa_signal_bot.providers.provider_interface import build_empty_provider_response
            response = build_empty_provider_response(
                request, provider.name(), ProviderResponseStatus.FAILED, f"Exception during fetch: {str(e)}"
            )

        # Apply calendar adjustment if calendar is available
        if self.calendar and response.status in [ProviderResponseStatus.SUCCESS, ProviderResponseStatus.PARTIAL]:
            from usa_signal_bot.calendar.provider_calendar_adapter import attach_calendar_metadata_to_provider_response
            response = attach_calendar_metadata_to_provider_response(response, self.calendar)

        score = score_provider_response_quality(response)

        if self.calendar and response.status in [ProviderResponseStatus.SUCCESS, ProviderResponseStatus.PARTIAL]:
            from usa_signal_bot.calendar.session_validation import validate_provider_response_calendar_alignment
            val_results = validate_provider_response_calendar_alignment(response, self.calendar)
            from usa_signal_bot.calendar.provider_calendar_adapter import provider_quality_with_calendar_adjustment
            score = provider_quality_with_calendar_adjustment(score, val_results)

        return response, score

    def should_accept_response(self, response: ProviderResponse, score: ProviderQualityScore) -> bool:
        if response.status not in [ProviderResponseStatus.SUCCESS, ProviderResponseStatus.PARTIAL]:
            return False
        if score.score is None:
            return False
        if score.score < self.min_quality_score:
            return False
        return True

    def should_try_fallback(self, response: ProviderResponse, score: ProviderQualityScore) -> bool:
        if not self.fallback_enabled:
            return False
        return not self.should_accept_response(response, score)

    def route(self, request: ProviderRequest) -> ProviderRoutingResult:
        if self.prefer_cache:
            return self.route_with_cache_first(request)
        return self.route_with_quality_threshold(request)

    def route_with_cache_first(self, request: ProviderRequest) -> ProviderRoutingResult:
        return self.route_with_quality_threshold(request) # Logic is same, order handles cache first

    def route_with_quality_threshold(self, request: ProviderRequest) -> ProviderRoutingResult:
        now_utc = datetime.now(timezone.utc).isoformat()

        order = self.build_provider_order(request)
        attempted = []
        scores = []

        best_response = None
        best_score = None

        for provider in order:
            attempted.append(provider.name())

            response, score = self.try_provider(provider, request)
            scores.append(score)

            if self.should_accept_response(response, score):
                decision = ProviderRoutingDecision.USE_CACHE if provider.name() == DataProviderName.LOCAL_CACHE else ProviderRoutingDecision.USE_PRIMARY
                if len(attempted) > 1:
                    decision = ProviderRoutingDecision.USE_FALLBACK

                return ProviderRoutingResult(
                    routing_id=create_provider_routing_id(),
                    created_at_utc=now_utc,
                    request=request,
                    decision=decision,
                    selected_provider=provider.name(),
                    attempted_providers=attempted,
                    quality_scores=scores,
                    fallback_used=len(attempted) > 1,
                    response=response
                )

            # Track best response so far even if it doesn't meet threshold
            if best_score is None or (score.score is not None and (best_score.score is None or score.score > best_score.score)):
                best_response = response
                best_score = score

            if not self.fallback_enabled:
                break

        # If we got here, no provider met the threshold
        return ProviderRoutingResult(
            routing_id=create_provider_routing_id(),
            created_at_utc=now_utc,
            request=request,
            decision=ProviderRoutingDecision.BLOCK,
            selected_provider=DataProviderName.UNKNOWN,
            attempted_providers=attempted,
            quality_scores=scores,
            fallback_used=False,
            response=best_response,
            errors=["No provider met the quality threshold"]
        )
