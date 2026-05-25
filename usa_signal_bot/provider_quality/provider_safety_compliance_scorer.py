import datetime
from typing import Dict, Optional

from usa_signal_bot.core.enums import DataQualityComponent, DataQualityGrade, ProviderQualityRiskFlag
from usa_signal_bot.provider_quality.phase109_models import DataQualityScoreComponent, create_data_quality_component_id

def provider_safety_compliance_grade(score: float) -> DataQualityGrade:
    if score >= 100:
        return DataQualityGrade.EXCELLENT
    return DataQualityGrade.BLOCKED

def provider_safety_compliance_score_from_flags(flags: Dict[str, bool]) -> float:
    # Any unsafe flag causes score = 0
    for v in flags.values():
        if v:
            return 0.0
    return 100.0

def score_provider_safety_compliance(
    provider_name: str,
    network_used: bool = False,
    paid_api_used: bool = False,
    scraping_used: bool = False,
    html_parsing_used: bool = False,
    broker_used: bool = False,
    order_created: bool = False,
    paper_state_mutated: bool = False,
    telegram_real_sent: bool = False,
    dashboard_started: bool = False,
    symbol: Optional[str] = None
) -> DataQualityScoreComponent:

    flags = {
        "network_used": network_used,
        "paid_api_used": paid_api_used,
        "scraping_used": scraping_used,
        "html_parsing_used": html_parsing_used,
        "broker_used": broker_used,
        "order_created": order_created,
        "paper_state_mutated": paper_state_mutated,
        "telegram_real_sent": telegram_real_sent,
        "dashboard_started": dashboard_started
    }

    score = provider_safety_compliance_score_from_flags(flags)
    grade = provider_safety_compliance_grade(score)

    risk_flags = []
    warnings = []
    errors = []

    if network_used: risk_flags.append(ProviderQualityRiskFlag.NETWORK_FETCH_ATTEMPTED); errors.append("network_used=True")
    if paid_api_used: risk_flags.append(ProviderQualityRiskFlag.PAID_API_RISK); errors.append("paid_api_used=True")
    if scraping_used: risk_flags.append(ProviderQualityRiskFlag.SCRAPING_RISK); errors.append("scraping_used=True")
    if html_parsing_used: risk_flags.append(ProviderQualityRiskFlag.HTML_PARSE_RISK); errors.append("html_parsing_used=True")
    if broker_used: risk_flags.append(ProviderQualityRiskFlag.BROKER_RISK); errors.append("broker_used=True")
    if order_created: risk_flags.append(ProviderQualityRiskFlag.ORDER_RISK); errors.append("order_created=True")
    if paper_state_mutated: risk_flags.append(ProviderQualityRiskFlag.PAPER_MUTATION_RISK); errors.append("paper_state_mutated=True")
    if telegram_real_sent: risk_flags.append(ProviderQualityRiskFlag.TELEGRAM_REAL_SEND_RISK); errors.append("telegram_real_sent=True")
    if dashboard_started: risk_flags.append(ProviderQualityRiskFlag.DASHBOARD_RISK); errors.append("dashboard_started=True")

    return DataQualityScoreComponent(
        component_id=create_data_quality_component_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        provider_name=provider_name,
        symbol=symbol,
        component=DataQualityComponent.SAFETY_COMPLIANCE,
        raw_value=None,
        score=score,
        weight=0.0,
        weighted_score=0.0,
        grade=grade,
        explanation=f"Safety Compliance scored {score:.1f}. Unsafe flags: {[k for k, v in flags.items() if v]}",
        risk_flags=risk_flags,
        warnings=warnings,
        errors=errors
    )

def provider_safety_compliance_to_text(component: DataQualityScoreComponent) -> str:
    return f"Safety Compliance: {component.score:.1f} ({component.grade.value}) - {component.explanation}"
