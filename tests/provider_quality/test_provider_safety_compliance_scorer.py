import pytest
from unittest.mock import patch
import datetime
from usa_signal_bot.provider_quality.provider_safety_compliance_scorer import (
    SafetyComplianceFlags,
    provider_safety_compliance_grade,
    provider_safety_compliance_score_from_flags,
    score_provider_safety_compliance,
    provider_safety_compliance_to_text,
)
from usa_signal_bot.core.enums import DataQualityGrade, ProviderQualityRiskFlag

def test_safety_compliance_flags_default():
    flags = SafetyComplianceFlags()
    assert flags.network_used is False
    assert flags.paid_api_used is False
    assert flags.scraping_used is False
    assert flags.html_parsing_used is False
    assert flags.broker_used is False
    assert flags.order_created is False
    assert flags.paper_state_mutated is False
    assert flags.telegram_real_sent is False
    assert flags.dashboard_started is False

    flags_dict = flags.to_dict()
    assert all(not v for v in flags_dict.values())

def test_provider_safety_compliance_grade():
    assert provider_safety_compliance_grade(100.0) == DataQualityGrade.EXCELLENT
    assert provider_safety_compliance_grade(150.0) == DataQualityGrade.EXCELLENT
    assert provider_safety_compliance_grade(99.9) == DataQualityGrade.BLOCKED
    assert provider_safety_compliance_grade(0.0) == DataQualityGrade.BLOCKED

def test_provider_safety_compliance_score_from_flags():
    # All false -> 100.0
    flags = SafetyComplianceFlags()
    assert provider_safety_compliance_score_from_flags(flags.to_dict()) == 100.0

    # One true -> 0.0
    flags.network_used = True
    assert provider_safety_compliance_score_from_flags(flags.to_dict()) == 0.0

@patch("usa_signal_bot.provider_quality.provider_safety_compliance_scorer.create_data_quality_component_id")
@patch("usa_signal_bot.provider_quality.provider_safety_compliance_scorer.datetime")
def test_score_provider_safety_compliance_clean(mock_datetime, mock_create_id):
    # Mocking
    mock_create_id.return_value = "dq_test_123"

    mock_now = datetime.datetime(2025, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
    mock_datetime.datetime.now.return_value = mock_now
    mock_datetime.timezone.utc = datetime.timezone.utc

    flags = SafetyComplianceFlags()
    result = score_provider_safety_compliance("test_provider", flags, "AAPL")

    assert result.provider_name == "test_provider"
    assert result.symbol == "AAPL"
    assert result.score == 100.0
    assert result.grade == DataQualityGrade.EXCELLENT
    assert not result.risk_flags
    assert not result.errors

    assert result.component_id == "dq_test_123"
    assert result.created_at_utc == "2025-01-01T12:00:00Z"

@patch("usa_signal_bot.provider_quality.provider_safety_compliance_scorer.create_data_quality_component_id")
@patch("usa_signal_bot.provider_quality.provider_safety_compliance_scorer.datetime")
def test_score_provider_safety_compliance_unsafe(mock_datetime, mock_create_id):
    # Mocking
    mock_create_id.return_value = "dq_test_456"

    mock_now = datetime.datetime(2025, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
    mock_datetime.datetime.now.return_value = mock_now
    mock_datetime.timezone.utc = datetime.timezone.utc

    flags = SafetyComplianceFlags(network_used=True, broker_used=True)
    result = score_provider_safety_compliance("test_provider", flags, "AAPL")

    assert result.score == 0.0
    assert result.grade == DataQualityGrade.BLOCKED
    assert ProviderQualityRiskFlag.NETWORK_FETCH_ATTEMPTED in result.risk_flags
    assert ProviderQualityRiskFlag.BROKER_RISK in result.risk_flags
    assert "network_used=True" in result.errors
    assert "broker_used=True" in result.errors
    assert len(result.risk_flags) == 2
    assert len(result.errors) == 2

    assert result.component_id == "dq_test_456"
    assert result.created_at_utc == "2025-01-01T12:00:00Z"

def test_score_provider_safety_compliance_all_flags():
    flags = SafetyComplianceFlags(
        network_used=True,
        paid_api_used=True,
        scraping_used=True,
        html_parsing_used=True,
        broker_used=True,
        order_created=True,
        paper_state_mutated=True,
        telegram_real_sent=True,
        dashboard_started=True,
    )
    result = score_provider_safety_compliance("test_provider", flags, "AAPL")

    assert result.score == 0.0
    assert result.grade == DataQualityGrade.BLOCKED
    assert len(result.risk_flags) == 9
    assert len(result.errors) == 9

def test_provider_safety_compliance_to_text():
    flags = SafetyComplianceFlags(network_used=True)
    result = score_provider_safety_compliance("test_provider", flags, "AAPL")
    text_output = provider_safety_compliance_to_text(result)
    assert text_output == "Safety Compliance: 0.0 (BLOCKED) - Safety Compliance scored 0.0. Unsafe flags: ['network_used']"

    flags_clean = SafetyComplianceFlags()
    result_clean = score_provider_safety_compliance("test_provider", flags_clean, "AAPL")
    text_output_clean = provider_safety_compliance_to_text(result_clean)
    assert text_output_clean == "Safety Compliance: 100.0 (EXCELLENT) - Safety Compliance scored 100.0. Unsafe flags: []"
