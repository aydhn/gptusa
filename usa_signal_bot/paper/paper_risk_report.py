from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from usa_signal_bot.paper.paper_models import VirtualAccount, PaperPosition
from usa_signal_bot.paper.paper_analytics_models import (
    PaperEquityMetrics,
    PaperExposureMetrics,
    PaperRiskMetrics,
)
from usa_signal_bot.core.enums import (
    PaperRiskLevel,
    PaperDrawdownStatus,
    PaperRiskLimitStatus,
    PaperMetricStatus
)
from usa_signal_bot.paper.paper_exposure_analytics import calculate_largest_position_weight

@dataclass
class PaperRiskLimitConfig:
    max_drawdown_warning_pct: float
    max_drawdown_breach_pct: float
    max_exposure_to_equity_pct: float
    min_cash_buffer_pct: float
    max_open_positions: int
    max_largest_position_weight: float
    max_daily_loss_pct: float

@dataclass
class PaperRiskLimitCheck:
    name: str
    status: PaperRiskLimitStatus
    risk_level: PaperRiskLevel
    observed_value: Optional[float]
    limit_value: Optional[float]
    message: str

@dataclass
class PaperRiskReport:
    report_id: str
    created_at_utc: str
    account_id: Optional[str]
    status: PaperRiskLimitStatus
    risk_level: PaperRiskLevel
    checks: List[PaperRiskLimitCheck]
    risk_metrics: PaperRiskMetrics
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def default_paper_risk_limit_config() -> PaperRiskLimitConfig:
    return PaperRiskLimitConfig(
        max_drawdown_warning_pct=10.0,
        max_drawdown_breach_pct=20.0,
        max_exposure_to_equity_pct=0.80,
        min_cash_buffer_pct=0.05,
        max_open_positions=20,
        max_largest_position_weight=0.15,
        max_daily_loss_pct=5.0
    )

def validate_paper_risk_limit_config(config: PaperRiskLimitConfig) -> None:
    if config.max_drawdown_warning_pct >= config.max_drawdown_breach_pct:
        raise ValueError("max_drawdown_warning_pct must be less than max_drawdown_breach_pct")

def check_paper_max_drawdown_limit(equity_metrics: PaperEquityMetrics, config: PaperRiskLimitConfig) -> PaperRiskLimitCheck:
    observed = equity_metrics.max_drawdown_pct
    if observed is None:
        return PaperRiskLimitCheck("Max Drawdown", PaperRiskLimitStatus.NOT_EVALUATED, PaperRiskLevel.UNKNOWN, None, config.max_drawdown_breach_pct, "No data")

    if observed >= config.max_drawdown_breach_pct:
        return PaperRiskLimitCheck("Max Drawdown", PaperRiskLimitStatus.BREACHED, PaperRiskLevel.HIGH, observed, config.max_drawdown_breach_pct, f"{observed:.2f}% >= {config.max_drawdown_breach_pct:.2f}%")
    if observed >= config.max_drawdown_warning_pct:
        return PaperRiskLimitCheck("Max Drawdown", PaperRiskLimitStatus.WARNING, PaperRiskLevel.MODERATE, observed, config.max_drawdown_warning_pct, f"{observed:.2f}% >= {config.max_drawdown_warning_pct:.2f}%")

    return PaperRiskLimitCheck("Max Drawdown", PaperRiskLimitStatus.WITHIN_LIMIT, PaperRiskLevel.LOW, observed, config.max_drawdown_breach_pct, "OK")

def check_paper_current_drawdown_limit(equity_metrics: PaperEquityMetrics, config: PaperRiskLimitConfig) -> PaperRiskLimitCheck:
    observed = equity_metrics.current_drawdown_pct
    if observed is None:
        return PaperRiskLimitCheck("Current Drawdown", PaperRiskLimitStatus.NOT_EVALUATED, PaperRiskLevel.UNKNOWN, None, config.max_drawdown_breach_pct, "No data")

    if observed >= config.max_drawdown_breach_pct:
        return PaperRiskLimitCheck("Current Drawdown", PaperRiskLimitStatus.BREACHED, PaperRiskLevel.HIGH, observed, config.max_drawdown_breach_pct, f"{observed:.2f}% >= {config.max_drawdown_breach_pct:.2f}%")
    if observed >= config.max_drawdown_warning_pct:
        return PaperRiskLimitCheck("Current Drawdown", PaperRiskLimitStatus.WARNING, PaperRiskLevel.MODERATE, observed, config.max_drawdown_warning_pct, f"{observed:.2f}% >= {config.max_drawdown_warning_pct:.2f}%")

    return PaperRiskLimitCheck("Current Drawdown", PaperRiskLimitStatus.WITHIN_LIMIT, PaperRiskLevel.LOW, observed, config.max_drawdown_breach_pct, "OK")

def check_paper_exposure_limit(exposure_metrics: PaperExposureMetrics, config: PaperRiskLimitConfig) -> PaperRiskLimitCheck:
    observed = exposure_metrics.exposure_to_equity_max
    if observed is None:
        return PaperRiskLimitCheck("Exposure to Equity", PaperRiskLimitStatus.NOT_EVALUATED, PaperRiskLevel.UNKNOWN, None, config.max_exposure_to_equity_pct, "No data")

    if observed > config.max_exposure_to_equity_pct:
        return PaperRiskLimitCheck("Exposure to Equity", PaperRiskLimitStatus.BREACHED, PaperRiskLevel.HIGH, observed, config.max_exposure_to_equity_pct, f"{observed*100:.2f}% > {config.max_exposure_to_equity_pct*100:.2f}%")

    return PaperRiskLimitCheck("Exposure to Equity", PaperRiskLimitStatus.WITHIN_LIMIT, PaperRiskLevel.LOW, observed, config.max_exposure_to_equity_pct, "OK")

def check_paper_cash_buffer(account: VirtualAccount, config: PaperRiskLimitConfig) -> PaperRiskLimitCheck:
    total_equity = account.equity
    if total_equity <= 0:
        return PaperRiskLimitCheck("Cash Buffer", PaperRiskLimitStatus.NOT_EVALUATED, PaperRiskLevel.UNKNOWN, None, config.min_cash_buffer_pct, "Invalid equity")

    observed = account.cash / total_equity
    if observed < config.min_cash_buffer_pct:
        return PaperRiskLimitCheck("Cash Buffer", PaperRiskLimitStatus.WARNING, PaperRiskLevel.MODERATE, observed, config.min_cash_buffer_pct, f"{observed*100:.2f}% < {config.min_cash_buffer_pct*100:.2f}%")

    return PaperRiskLimitCheck("Cash Buffer", PaperRiskLimitStatus.WITHIN_LIMIT, PaperRiskLevel.LOW, observed, config.min_cash_buffer_pct, "OK")

def check_paper_open_positions(exposure_metrics: PaperExposureMetrics, config: PaperRiskLimitConfig) -> PaperRiskLimitCheck:
    observed = exposure_metrics.final_open_positions
    if observed > config.max_open_positions:
        return PaperRiskLimitCheck("Open Positions", PaperRiskLimitStatus.BREACHED, PaperRiskLevel.HIGH, float(observed), float(config.max_open_positions), f"{observed} > {config.max_open_positions}")
    return PaperRiskLimitCheck("Open Positions", PaperRiskLimitStatus.WITHIN_LIMIT, PaperRiskLevel.LOW, float(observed), float(config.max_open_positions), "OK")

def check_paper_largest_position_weight(positions: List[PaperPosition], equity: Optional[float], config: PaperRiskLimitConfig) -> PaperRiskLimitCheck:
    observed = calculate_largest_position_weight(positions, equity)
    if observed is None:
        return PaperRiskLimitCheck("Largest Position Weight", PaperRiskLimitStatus.NOT_EVALUATED, PaperRiskLevel.UNKNOWN, None, config.max_largest_position_weight, "No data")

    if observed > config.max_largest_position_weight:
        return PaperRiskLimitCheck("Largest Position Weight", PaperRiskLimitStatus.BREACHED, PaperRiskLevel.HIGH, observed, config.max_largest_position_weight, f"{observed*100:.2f}% > {config.max_largest_position_weight*100:.2f}%")

    return PaperRiskLimitCheck("Largest Position Weight", PaperRiskLimitStatus.WITHIN_LIMIT, PaperRiskLevel.LOW, observed, config.max_largest_position_weight, "OK")

def build_paper_risk_metrics(account: VirtualAccount, equity_metrics: PaperEquityMetrics, exposure_metrics: PaperExposureMetrics, positions: List[PaperPosition], config: Optional[PaperRiskLimitConfig] = None) -> PaperRiskMetrics:
    if config is None:
        config = default_paper_risk_limit_config()

    checks = [
        check_paper_max_drawdown_limit(equity_metrics, config),
        check_paper_current_drawdown_limit(equity_metrics, config),
        check_paper_exposure_limit(exposure_metrics, config),
        check_paper_cash_buffer(account, config),
        check_paper_open_positions(exposure_metrics, config),
        check_paper_largest_position_weight(positions, account.equity, config)
    ]

    risk_level = PaperRiskLevel.LOW
    status = PaperRiskLimitStatus.WITHIN_LIMIT
    concentration_warning = False

    for check in checks:
        if check.risk_level == PaperRiskLevel.CRITICAL:
            risk_level = PaperRiskLevel.CRITICAL
            status = PaperRiskLimitStatus.CRITICAL
        elif check.risk_level == PaperRiskLevel.HIGH and risk_level != PaperRiskLevel.CRITICAL:
            risk_level = PaperRiskLevel.HIGH
            status = PaperRiskLimitStatus.BREACHED
        elif check.risk_level == PaperRiskLevel.MODERATE and risk_level not in [PaperRiskLevel.CRITICAL, PaperRiskLevel.HIGH]:
            risk_level = PaperRiskLevel.MODERATE
            if status == PaperRiskLimitStatus.WITHIN_LIMIT:
                status = PaperRiskLimitStatus.WARNING

        if check.name == "Largest Position Weight" and check.status in [PaperRiskLimitStatus.WARNING, PaperRiskLimitStatus.BREACHED, PaperRiskLimitStatus.CRITICAL]:
            concentration_warning = True

    # Drawdown status mapping
    dd_status = PaperDrawdownStatus.NORMAL
    if equity_metrics.current_drawdown_pct is not None:
        if equity_metrics.current_drawdown_pct >= config.max_drawdown_breach_pct:
            dd_status = PaperDrawdownStatus.BREACH
        elif equity_metrics.current_drawdown_pct >= config.max_drawdown_warning_pct:
            dd_status = PaperDrawdownStatus.WARNING

    return PaperRiskMetrics(
        status=PaperMetricStatus.OK,
        risk_level=risk_level,
        drawdown_status=dd_status,
        risk_limit_status=status,
        max_drawdown_pct=equity_metrics.max_drawdown_pct,
        current_drawdown_pct=equity_metrics.current_drawdown_pct,
        exposure_to_equity_max=exposure_metrics.exposure_to_equity_max,
        cash_buffer_pct=account.cash / account.equity if account.equity > 0 else None,
        open_position_count=len(positions),
        largest_position_weight=calculate_largest_position_weight(positions, account.equity),
        concentration_warning=concentration_warning,
        warnings=[],
        errors=[]
    )

def build_paper_risk_report(account: VirtualAccount, equity_metrics: PaperEquityMetrics, exposure_metrics: PaperExposureMetrics, positions: List[PaperPosition], config: Optional[PaperRiskLimitConfig] = None) -> PaperRiskReport:
    if config is None:
        config = default_paper_risk_limit_config()

    checks = [
        check_paper_max_drawdown_limit(equity_metrics, config),
        check_paper_current_drawdown_limit(equity_metrics, config),
        check_paper_exposure_limit(exposure_metrics, config),
        check_paper_cash_buffer(account, config),
        check_paper_open_positions(exposure_metrics, config),
        check_paper_largest_position_weight(positions, account.equity, config)
    ]

    risk_metrics = build_paper_risk_metrics(account, equity_metrics, exposure_metrics, positions, config)

    return PaperRiskReport(
        report_id=f"risk_report_{datetime.now(timezone.utc).timestamp()}",
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        account_id=account.account_id,
        status=risk_metrics.risk_limit_status,
        risk_level=risk_metrics.risk_level,
        checks=checks,
        risk_metrics=risk_metrics,
        warnings=[],
        errors=[]
    )

def paper_risk_limit_check_to_dict(check: PaperRiskLimitCheck) -> Dict[str, Any]:
    return {
        "name": check.name,
        "status": check.status.value,
        "risk_level": check.risk_level.value,
        "observed_value": check.observed_value,
        "limit_value": check.limit_value,
        "message": check.message
    }

def paper_risk_report_to_dict(report: PaperRiskReport) -> Dict[str, Any]:
    from usa_signal_bot.paper.paper_analytics_models import paper_risk_metrics_to_dict
    return {
        "report_id": report.report_id,
        "created_at_utc": report.created_at_utc,
        "account_id": report.account_id,
        "status": report.status.value,
        "risk_level": report.risk_level.value,
        "checks": [paper_risk_limit_check_to_dict(c) for c in report.checks],
        "risk_metrics": paper_risk_metrics_to_dict(report.risk_metrics),
        "warnings": report.warnings,
        "errors": report.errors
    }

def paper_risk_report_to_text(report: PaperRiskReport) -> str:
    lines = [
        "--- Paper Risk Report ---",
        f"Status: {report.status.value}",
        f"Risk Level: {report.risk_level.value}",
        "\nChecks:"
    ]
    for check in report.checks:
        lines.append(f"- {check.name} [{check.status.value}]: {check.message}")

    if report.warnings:
        lines.append("\nWarnings: " + ", ".join(report.warnings))
    if report.errors:
        lines.append("\nErrors: " + ", ".join(report.errors))

    lines.append("")
    return "\n".join(lines)
