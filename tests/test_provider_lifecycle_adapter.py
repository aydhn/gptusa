import pytest
from usa_signal_bot.universe_lifecycle.provider_lifecycle_adapter import (
    attach_lifecycle_metadata_to_provider_response, lifecycle_quality_adjustment_for_response,
    provider_quality_with_lifecycle_adjustment, provider_response_symbols_requiring_review
)
from usa_signal_bot.providers.provider_models import ProviderResponse
from usa_signal_bot.providers.provider_quality import ProviderQualityScore
from usa_signal_bot.universe_lifecycle.symbol_status_resolver import SymbolStatusResolver
from usa_signal_bot.universe_lifecycle.lifecycle_models import SymbolLifecycleRecord
from usa_signal_bot.core.enums import SymbolLifecycleStatus, SymbolLifecycleSource, ProviderResponseStatus, ProviderQualityStatus

def test_attach_lifecycle_metadata():
    r1 = SymbolLifecycleRecord("AAPL", SymbolLifecycleStatus.ACTIVE, SymbolLifecycleSource.MANUAL_REGISTRY)
    resolver = SymbolStatusResolver([r1])

    resp = ProviderResponse(response_id="1", request_id="2", provider_name="prov", status=ProviderResponseStatus.SUCCESS, created_at_utc="now", symbol_count=1, row_count=0, data={"AAPL": []})
    resp = attach_lifecycle_metadata_to_provider_response(resp, resolver)

    assert "lifecycle_status" in resp.metadata
    assert resp.metadata["lifecycle_status"]["AAPL"] == "ACTIVE"

def test_lifecycle_quality_adjustment_delisted():
    r1 = SymbolLifecycleRecord("TWTR", SymbolLifecycleStatus.DELISTED, SymbolLifecycleSource.MANUAL_REGISTRY)
    resolver = SymbolStatusResolver([r1])

    resp = ProviderResponse(response_id="1", request_id="2", provider_name="prov", status=ProviderResponseStatus.SUCCESS, created_at_utc="now", symbol_count=1, row_count=0, data={"TWTR": []})
    adj = lifecycle_quality_adjustment_for_response(resp, resolver)

    assert adj["adjustment_score"] < 0
    assert "delisted" in adj["reason"]

def test_provider_quality_with_adjustment():
    r1 = SymbolLifecycleRecord("TWTR", SymbolLifecycleStatus.DELISTED, SymbolLifecycleSource.MANUAL_REGISTRY)
    resolver = SymbolStatusResolver([r1])

    resp = ProviderResponse(response_id="1", request_id="2", provider_name="prov", status=ProviderResponseStatus.SUCCESS, created_at_utc="now", symbol_count=1, row_count=0, data={"TWTR": []})

    class MockScore:
        def __init__(self):
            self.score = 100.0
            self.summary = "ok"
    score = MockScore()


    score = provider_quality_with_lifecycle_adjustment(score, resp, resolver)
    assert score.score < 100.0
    assert "Lifecycle Adjusted" in score.summary

def test_symbols_requiring_review():
    r1 = SymbolLifecycleRecord("AAPL", SymbolLifecycleStatus.ACTIVE, SymbolLifecycleSource.MANUAL_REGISTRY)
    resolver = SymbolStatusResolver([r1]) # Missing TWTR

    resp = ProviderResponse(response_id="1", request_id="2", provider_name="prov", status=ProviderResponseStatus.SUCCESS, created_at_utc="now", symbol_count=1, row_count=0, data={"AAPL": [], "TWTR": []})
    req = provider_response_symbols_requiring_review(resp, resolver)

    assert req == ["TWTR"]
