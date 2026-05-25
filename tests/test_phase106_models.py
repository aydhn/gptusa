
import pytest
from usa_signal_bot.data_providers.phase106_models import (
    ProviderKickoffGateIngestionResult, validate_provider_kickoff_gate_ingestion_result,
    ProviderSelectionRequest, validate_provider_selection_request
)
from usa_signal_bot.core.exceptions import ProviderValidationError

def test_kickoff_gate_ingestion_result_validation():
    valid_res = ProviderKickoffGateIngestionResult(
        ingestion_id="i1", created_at_utc="2023", source_path=None, source_review_id=None, source_gate_id=None,
        available=True, provider_ready=True, ready_for_phase106=True, phase106_scope_allowed=True,
        metadata_only=True, activation_allowed=False, active_paper_enabled=False, broker_execution_enabled=False,
        paper_state_mutation_enabled=False, telegram_real_send_enabled=False, scraping_enabled=False,
        html_parse_enabled=False, dashboard_enabled=False, paid_api_enabled=False, provider_network_fetch_required=False,
        valid_for_phase106=True
    )
    validate_provider_kickoff_gate_ingestion_result(valid_res) # Should not raise

    invalid_res = valid_res
    invalid_res.broker_execution_enabled = True
    with pytest.raises(ProviderValidationError):
        validate_provider_kickoff_gate_ingestion_result(invalid_res)

def test_selection_request_validation():
    from usa_signal_bot.core.enums import DataProviderKind, DataProviderCapability, ProviderDataDomain, ProviderSelectorMode
    valid_req = ProviderSelectionRequest(
        selection_id="s1", created_at_utc="2023", provider_kind=DataProviderKind.MARKET_DATA,
        capability=DataProviderCapability.GET_DAILY_OHLCV, domain=ProviderDataDomain.EQUITY_US,
        selector_mode=ProviderSelectorMode.METADATA_ONLY, symbol=None, metadata_only=True,
        allow_network=False, allow_paid_api=False, allow_scraping=False, allow_broker=False, allow_order=False
    )
    validate_provider_selection_request(valid_req) # Should not raise

    invalid_req = valid_req
    invalid_req.allow_network = True
    with pytest.raises(ProviderValidationError):
        validate_provider_selection_request(invalid_req)
