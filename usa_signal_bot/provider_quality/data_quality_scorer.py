import datetime
from typing import List, Dict, Any, Optional

from usa_signal_bot.core.enums import (
    DataQualityGrade,
    ProviderQualityRiskFlag,
    DataQualityComponent,
)
from usa_signal_bot.provider_quality.phase109_models import (
    ProviderDataQualityScore,
    DataQualityScoreComponent,
    create_provider_data_quality_score_id,
)
from usa_signal_bot.provider_quality.scoring_policy import (
    build_default_provider_quality_scoring_policy,
    normalize_scoring_weights,
    scoring_policy_component_weight,
)

from usa_signal_bot.provider_quality.completeness_scorer import score_completeness
from usa_signal_bot.provider_quality.freshness_scorer import score_freshness
from usa_signal_bot.provider_quality.schema_validity_scorer import score_schema_validity
from usa_signal_bot.provider_quality.continuity_scorer import score_continuity
from usa_signal_bot.provider_quality.source_disagreement_scorer import (
    score_source_agreement,
)
from usa_signal_bot.provider_quality.outlier_penalty_scorer import score_outlier_profile
from usa_signal_bot.provider_quality.cache_reliability_scorer import (
    score_cache_reliability,
)
from usa_signal_bot.provider_quality.provider_safety_compliance_scorer import (
    score_provider_safety_compliance,
    SafetyComplianceFlags,
)


def data_quality_grade_from_score(
    score: float, blocked: bool = False
) -> DataQualityGrade:
    if blocked:
        return DataQualityGrade.BLOCKED
    if score >= 90:
        return DataQualityGrade.EXCELLENT
    if score >= 80:
        return DataQualityGrade.GOOD
    if score >= 65:
        return DataQualityGrade.ACCEPTABLE
    if score >= 40:
        return DataQualityGrade.WEAK
    return DataQualityGrade.POOR


def aggregate_quality_components(
    provider_name: str,
    symbol: Optional[str],
    capability: str,
    components: List[DataQualityScoreComponent],
    policy: Optional[Dict[str, float]] = None,
) -> ProviderDataQualityScore:

    if policy is None:
        policy = build_default_provider_quality_scoring_policy()

    normalized_policy = normalize_scoring_weights(policy)

    total_score = 0.0
    risk_flags = []
    warnings = []
    errors = []
    blocked = False

    for c in components:
        w = scoring_policy_component_weight(c.component, normalized_policy)
        c.weight = w
        c.weighted_score = c.score * w
        total_score += c.weighted_score

        risk_flags.extend(c.risk_flags)
        warnings.extend(c.warnings)
        errors.extend(c.errors)

        if c.component == DataQualityComponent.SAFETY_COMPLIANCE and c.score == 0:
            blocked = True
        if c.component == DataQualityComponent.SCHEMA_VALIDITY and c.score == 0:
            blocked = True

    # Deduplicate risk flags
    risk_flags = list(set(risk_flags))

    total_score = max(0.0, min(100.0, total_score))
    grade = data_quality_grade_from_score(total_score, blocked)

    usable_for_research = not blocked and total_score >= 65.0
    use_with_warning = not blocked and 40.0 <= total_score < 65.0

    return ProviderDataQualityScore(
        score_id=create_provider_data_quality_score_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        provider_name=provider_name,
        symbol=symbol,
        capability=capability,
        components=components,
        total_score=total_score,
        grade=grade,
        usable_for_research=usable_for_research,
        use_with_warning=use_with_warning,
        blocked=blocked,
        explanation=f"Aggregated score {total_score:.1f}. Usable: {usable_for_research}.",
        risk_flags=risk_flags,
        warnings=warnings,
        errors=errors,
    )


def build_provider_data_quality_score(
    provider_name: str,
    symbol: Optional[str],
    capability: str,
    records: Optional[List[Dict[str, Any]]] = None,
    schema_errors: Optional[List[str]] = None,
    freshness_payload: Optional[Dict[str, Any]] = None,
    source_comparison_payload: Optional[Dict[str, Any]] = None,
    cache_payload: Optional[Dict[str, Any]] = None,
    safety_payload: Optional[Dict[str, Any]] = None,
    policy: Optional[Dict[str, float]] = None,
) -> ProviderDataQualityScore:

    records = records or []
    schema_errors = schema_errors or []
    f_payload = freshness_payload or {"fresh": False, "stale": False}
    sc_payload = source_comparison_payload or {"disagreement_score": None}
    c_payload = cache_payload or {
        "status": "UNKNOWN",
        "checksum_present": False,
        "schema_valid": len(schema_errors) == 0,
    }
    saf_payload = safety_payload or {}

    c_comp = score_completeness(records, provider_name=provider_name, symbol=symbol)
    f_comp = score_freshness(
        f_payload.get("fresh", False),
        f_payload.get("stale", False),
        f_payload.get("expired", False),
        f_payload.get("age_seconds"),
        f_payload.get("ttl_seconds"),
        provider_name=provider_name,
        symbol=symbol,
    )
    sv_comp = score_schema_validity(
        schema_errors, provider_name=provider_name, symbol=symbol
    )
    cont_comp = score_continuity(
        records, expected_interval="1d", provider_name=provider_name, symbol=symbol
    )
    sa_comp = score_source_agreement(
        sc_payload.get("disagreement_score"),
        sc_payload.get("status"),
        provider_name=provider_name,
        symbol=symbol,
    )
    out_comp = score_outlier_profile(
        records, provider_name=provider_name, symbol=symbol
    )
    cr_comp = score_cache_reliability(
        c_payload.get("status"),
        c_payload.get("checksum_present", False),
        c_payload.get("schema_valid", True),
        provider_name=provider_name,
        symbol=symbol,
    )
    saf_flags = SafetyComplianceFlags(
        network_used=saf_payload.get("network_used", False),
        paid_api_used=saf_payload.get("paid_api_used", False),
        scraping_used=saf_payload.get("scraping_used", False),
        html_parsing_used=saf_payload.get("html_parsing_used", False),
        broker_used=saf_payload.get("broker_used", False),
        order_created=saf_payload.get("order_created", False),
        paper_state_mutated=saf_payload.get("paper_state_mutated", False),
        telegram_real_sent=saf_payload.get("telegram_real_sent", False),
        dashboard_started=saf_payload.get("dashboard_started", False),
    )
    sf_comp = score_provider_safety_compliance(
        provider_name, flags=saf_flags, symbol=symbol
    )

    components = [
        c_comp,
        f_comp,
        sv_comp,
        cont_comp,
        sa_comp,
        out_comp,
        cr_comp,
        sf_comp,
    ]

    return aggregate_quality_components(
        provider_name, symbol, capability, components, policy
    )


def data_quality_score_summary(score: ProviderDataQualityScore) -> Dict[str, Any]:
    return {
        "score_id": score.score_id,
        "provider": score.provider_name,
        "symbol": score.symbol,
        "total_score": score.total_score,
        "grade": score.grade.value,
        "usable_for_research": score.usable_for_research,
        "blocked": score.blocked,
        "components": {c.component.value: c.score for c in score.components},
    }


def provider_data_quality_score_to_text(
    score: ProviderDataQualityScore, limit: int = 100
) -> str:
    lines = [
        f"Provider Data Quality Score: {score.provider_name} | Symbol: {score.symbol}",
        f"Total Score: {score.total_score:.1f} ({score.grade.value})",
        f"Blocked: {score.blocked} | Usable for Research: {score.usable_for_research}",
        f"Explanation: {score.explanation}",
        "Components:",
    ]
    for c in score.components:
        lines.append(f"  - {c.component.value}: {c.score:.1f} (Weight: {c.weight:.2f})")
    return "\n".join(lines)
