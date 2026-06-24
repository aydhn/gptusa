import datetime
from dataclasses import dataclass
from typing import Dict, Optional
import datetime

from usa_signal_bot.core.enums import (
    DataQualityComponent,
    DataQualityGrade,
    ProviderQualityRiskFlag,
)
from usa_signal_bot.provider_quality.phase109_models import (
    DataQualityScoreComponent,
    create_data_quality_component_id,
)


@dataclass
class SafetyComplianceFlags:
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    telegram_real_sent: bool = False
    dashboard_started: bool = False

    def to_dict(self) -> Dict[str, bool]:
        return {
            "network_used": self.network_used,
            "paid_api_used": self.paid_api_used,
            "scraping_used": self.scraping_used,
            "html_parsing_used": self.html_parsing_used,
            "broker_used": self.broker_used,
            "order_created": self.order_created,
            "paper_state_mutated": self.paper_state_mutated,
            "telegram_real_sent": self.telegram_real_sent,
            "dashboard_started": self.dashboard_started,
        }


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
    provider_name: str, flags: SafetyComplianceFlags, symbol: Optional[str] = None
) -> DataQualityScoreComponent:

    flags_dict = flags.to_dict()

    score = provider_safety_compliance_score_from_flags(flags_dict)
    grade = provider_safety_compliance_grade(score)

    risk_flags = []
    warnings = []
    errors = []

    if flags.network_used:
        risk_flags.append(ProviderQualityRiskFlag.NETWORK_FETCH_ATTEMPTED)
        errors.append("network_used=True")
    if flags.paid_api_used:
        risk_flags.append(ProviderQualityRiskFlag.PAID_API_RISK)
        errors.append("paid_api_used=True")
    if flags.scraping_used:
        risk_flags.append(ProviderQualityRiskFlag.SCRAPING_RISK)
        errors.append("scraping_used=True")
    if flags.html_parsing_used:
        risk_flags.append(ProviderQualityRiskFlag.HTML_PARSE_RISK)
        errors.append("html_parsing_used=True")
    if flags.broker_used:
        risk_flags.append(ProviderQualityRiskFlag.BROKER_RISK)
        errors.append("broker_used=True")
    if flags.order_created:
        risk_flags.append(ProviderQualityRiskFlag.ORDER_RISK)
        errors.append("order_created=True")
    if flags.paper_state_mutated:
        risk_flags.append(ProviderQualityRiskFlag.PAPER_MUTATION_RISK)
        errors.append("paper_state_mutated=True")
    if flags.telegram_real_sent:
        risk_flags.append(ProviderQualityRiskFlag.TELEGRAM_REAL_SEND_RISK)
        errors.append("telegram_real_sent=True")
    if flags.dashboard_started:
        risk_flags.append(ProviderQualityRiskFlag.DASHBOARD_RISK)
        errors.append("dashboard_started=True")

    return DataQualityScoreComponent(
        component_id=create_data_quality_component_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        provider_name=provider_name,
        symbol=symbol,
        component=DataQualityComponent.SAFETY_COMPLIANCE,
        raw_value=None,
        score=score,
        weight=0.0,
        weighted_score=0.0,
        grade=grade,
        explanation=f"Safety Compliance scored {score:.1f}. Unsafe flags: {[k for k, v in flags_dict.items() if v]}",
        risk_flags=risk_flags,
        warnings=warnings,
        errors=errors,
    )


def provider_safety_compliance_to_text(component: DataQualityScoreComponent) -> str:
    return f"Safety Compliance: {component.score:.1f} ({component.grade.value}) - {component.explanation}"
