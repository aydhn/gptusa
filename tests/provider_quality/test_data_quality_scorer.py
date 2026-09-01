import pytest
import datetime
from usa_signal_bot.core.enums import DataQualityGrade, DataQualityComponent
from usa_signal_bot.provider_quality.phase109_models import (
    ProviderDataQualityScore,
    DataQualityScoreComponent,
    ProviderQualityRiskFlag
)
from usa_signal_bot.provider_quality.data_quality_scorer import (
    data_quality_grade_from_score,
    aggregate_quality_components,
    build_provider_data_quality_score,
    ProviderDataQualityScoreParams,
    data_quality_score_summary,
    provider_data_quality_score_to_text,
)

def test_data_quality_grade_from_score():
    assert data_quality_grade_from_score(95.0) == DataQualityGrade.EXCELLENT
    assert data_quality_grade_from_score(85.0) == DataQualityGrade.GOOD
    assert data_quality_grade_from_score(70.0) == DataQualityGrade.ACCEPTABLE
    assert data_quality_grade_from_score(50.0) == DataQualityGrade.WEAK
    assert data_quality_grade_from_score(30.0) == DataQualityGrade.POOR
    assert data_quality_grade_from_score(95.0, blocked=True) == DataQualityGrade.BLOCKED

def test_aggregate_quality_components():
    components = [
        DataQualityScoreComponent(
            component_id="test",
            created_at_utc="2023-01-01T00:00:00Z",
            provider_name="test_provider",
            symbol="AAPL",
            component=DataQualityComponent.COMPLETENESS,
            score=100.0,
            raw_value=1.0,
            grade=DataQualityGrade.EXCELLENT,
            explanation="test",
            weight=0.0,
            weighted_score=0.0,
            risk_flags=[],
            warnings=[],
            errors=[],
        ),
    ]

    score = aggregate_quality_components(
        provider_name="test_provider",
        symbol="AAPL",
        capability="test",
        components=components,
    )

    assert isinstance(score, ProviderDataQualityScore)
    assert score.provider_name == "test_provider"
    assert score.symbol == "AAPL"
    assert score.capability == "test"
    assert score.total_score == 20.0
    assert score.grade == DataQualityGrade.POOR
    assert not score.usable_for_research

def test_aggregate_quality_components_blocked():
    components = [
        DataQualityScoreComponent(
            component_id="test",
            created_at_utc="2023-01-01T00:00:00Z",
            provider_name="test_provider",
            symbol="AAPL",
            component=DataQualityComponent.SAFETY_COMPLIANCE,
            score=0.0,
            raw_value=0.0,
            grade=DataQualityGrade.POOR,
            explanation="test",
            weight=0.0,
            weighted_score=0.0,
            risk_flags=[],
            warnings=[],
            errors=[],
        ),
    ]

    score = aggregate_quality_components(
        provider_name="test_provider",
        symbol="AAPL",
        capability="test",
        components=components,
    )

    assert score.blocked is True
    assert score.grade == DataQualityGrade.BLOCKED

def test_build_provider_data_quality_score():
    params = ProviderDataQualityScoreParams(
        provider_name="test",
        symbol="AAPL",
        capability="test",
        records=[{"time": "2023-01-01T00:00:00Z"}],
    )
    score = build_provider_data_quality_score(params)
    assert isinstance(score, ProviderDataQualityScore)

def test_data_quality_score_summary():
    score = ProviderDataQualityScore(
        score_id="test_id",
        created_at_utc="2023-01-01T00:00:00Z",
        provider_name="test",
        symbol="AAPL",
        capability="test",
        components=[],
        total_score=95.0,
        grade=DataQualityGrade.EXCELLENT,
        usable_for_research=True,
        use_with_warning=False,
        blocked=False,
        explanation="",
        risk_flags=[],
        warnings=[],
        errors=[],
    )

    summary = data_quality_score_summary(score)
    assert summary["score_id"] == "test_id"
    assert summary["provider"] == "test"
    assert summary["symbol"] == "AAPL"
    assert summary["total_score"] == 95.0
    assert summary["grade"] == DataQualityGrade.EXCELLENT.value
    assert summary["usable_for_research"] is True
    assert summary["blocked"] is False

def test_provider_data_quality_score_to_text():
    score = ProviderDataQualityScore(
        score_id="test_id",
        created_at_utc="2023-01-01T00:00:00Z",
        provider_name="test",
        symbol="AAPL",
        capability="test",
        components=[],
        total_score=95.0,
        grade=DataQualityGrade.EXCELLENT,
        usable_for_research=True,
        use_with_warning=False,
        blocked=False,
        explanation="Test explanation",
        risk_flags=[],
        warnings=[],
        errors=[],
    )

    text = provider_data_quality_score_to_text(score)
    assert "Provider Data Quality Score: test | Symbol: AAPL" in text
    assert "Total Score: 95.0 (EXCELLENT)" in text
    assert "Blocked: False | Usable for Research: True" in text
    assert "Explanation: Test explanation" in text

if __name__ == '__main__':
    pytest.main([__file__])
