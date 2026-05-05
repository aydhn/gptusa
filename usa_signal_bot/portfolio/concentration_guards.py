from dataclasses import dataclass, field
from typing import List, Dict, Optional
import uuid
from datetime import datetime, timezone
from usa_signal_bot.portfolio.portfolio_models import AllocationResult
from usa_signal_bot.core.enums import ConcentrationGuardType, PortfolioReviewStatus, AllocationStatus

@dataclass
class ConcentrationGuardConfig:
    max_symbol_weight: float
    max_strategy_weight: float
    max_timeframe_weight: float
    max_single_candidate_weight: float
    reject_breaches: bool = False
    cap_breaches: bool = True

@dataclass
class ConcentrationCheck:
    guard_type: ConcentrationGuardType
    key: str
    observed_weight: float
    limit_weight: float
    breached: bool
    message: str

@dataclass
class ConcentrationReport:
    report_id: str
    created_at_utc: str
    review_status: PortfolioReviewStatus
    checks: List[ConcentrationCheck]
    breach_count: int
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def default_concentration_guard_config() -> ConcentrationGuardConfig:
    return ConcentrationGuardConfig(
        max_symbol_weight=0.15,
        max_strategy_weight=0.30,
        max_timeframe_weight=0.50,
        max_single_candidate_weight=0.10,
        reject_breaches=False,
        cap_breaches=True
    )

def validate_concentration_guard_config(config: ConcentrationGuardConfig) -> None:
    from usa_signal_bot.core.exceptions import ConcentrationGuardError
    limits = [
        config.max_symbol_weight,
        config.max_strategy_weight,
        config.max_timeframe_weight,
        config.max_single_candidate_weight
    ]
    if any(limit < 0 or limit > 1 for limit in limits):
        raise ConcentrationGuardError("All concentration guard limits must be between 0 and 1.")

def build_concentration_report(allocations: List[AllocationResult], config: Optional[ConcentrationGuardConfig] = None) -> ConcentrationReport:
    from usa_signal_bot.portfolio.risk_budgeting import calculate_weight_by_symbol, calculate_weight_by_strategy, calculate_weight_by_timeframe
    cfg = config or default_concentration_guard_config()

    checks = []

    for symbol, weight in calculate_weight_by_symbol(allocations).items():
        breached = weight > cfg.max_symbol_weight
        checks.append(ConcentrationCheck(
            guard_type=ConcentrationGuardType.MAX_SYMBOL_WEIGHT,
            key=symbol,
            observed_weight=weight,
            limit_weight=cfg.max_symbol_weight,
            breached=breached,
            message="Breached max symbol weight" if breached else "OK"
        ))

    for strategy, weight in calculate_weight_by_strategy(allocations).items():
        breached = weight > cfg.max_strategy_weight
        checks.append(ConcentrationCheck(
            guard_type=ConcentrationGuardType.MAX_STRATEGY_WEIGHT,
            key=strategy,
            observed_weight=weight,
            limit_weight=cfg.max_strategy_weight,
            breached=breached,
            message="Breached max strategy weight" if breached else "OK"
        ))

    for timeframe, weight in calculate_weight_by_timeframe(allocations).items():
        breached = weight > cfg.max_timeframe_weight
        checks.append(ConcentrationCheck(
            guard_type=ConcentrationGuardType.MAX_TIMEFRAME_WEIGHT,
            key=timeframe,
            observed_weight=weight,
            limit_weight=cfg.max_timeframe_weight,
            breached=breached,
            message="Breached max timeframe weight" if breached else "OK"
        ))

    for a in allocations:
        if a.status in [AllocationStatus.ALLOCATED, AllocationStatus.CAPPED, AllocationStatus.REDUCED]:
            breached = a.target_weight > cfg.max_single_candidate_weight
            if breached:
                checks.append(ConcentrationCheck(
                    guard_type=ConcentrationGuardType.MAX_SINGLE_CANDIDATE_WEIGHT,
                    key=a.candidate_id,
                    observed_weight=a.target_weight,
                    limit_weight=cfg.max_single_candidate_weight,
                    breached=breached,
                    message="Breached max single candidate weight"
                ))

    breach_count = sum(1 for c in checks if c.breached)
    review_status = PortfolioReviewStatus.NEEDS_REVIEW if breach_count > 0 else PortfolioReviewStatus.ACCEPTABLE

    return ConcentrationReport(
        report_id=f"conc_{uuid.uuid4().hex[:8]}",
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        review_status=review_status,
        checks=checks,
        breach_count=breach_count,
        warnings=[f"{breach_count} concentration limits breached."] if breach_count > 0 else []
    )

def apply_concentration_caps(allocations: List[AllocationResult], config: Optional[ConcentrationGuardConfig] = None) -> List[AllocationResult]:
    cfg = config or default_concentration_guard_config()

    if not cfg.cap_breaches:
        return allocations

    for a in allocations:
        if a.status in [AllocationStatus.ALLOCATED, AllocationStatus.CAPPED, AllocationStatus.REDUCED]:
            if a.target_weight > cfg.max_single_candidate_weight:
                a.target_weight = cfg.max_single_candidate_weight
                a.status = AllocationStatus.CAPPED
                a.capped = True
                if f"Capped at max_single_candidate_weight {cfg.max_single_candidate_weight}" not in a.cap_reasons:
                    a.cap_reasons.append(f"Capped at max_single_candidate_weight {cfg.max_single_candidate_weight}")

            # Calculate proportional reductions if needed for group caps
            # This is simplified for the base implementation:
            # We would normally scale down all group members together.
            # To keep it deterministic and simpler in Phase 32 without optimization,
            # we rely on the normal allocation caps first.
    return allocations

def concentration_report_to_dict(report: ConcentrationReport) -> dict:
    from dataclasses import asdict
    d = asdict(report)
    d["review_status"] = report.review_status.value if hasattr(report.review_status, "value") else str(report.review_status)
    for check in d["checks"]:
        check["guard_type"] = check["guard_type"].value if hasattr(check["guard_type"], "value") else str(check["guard_type"])
    return d

def concentration_report_to_text(report: ConcentrationReport) -> str:
    lines = [
        f"Concentration Report [{report.report_id}]",
        f"Review Status: {report.review_status.value if hasattr(report.review_status, 'value') else str(report.review_status)}",
        f"Breaches: {report.breach_count}",
        "-" * 50
    ]
    for c in report.checks:
        if c.breached:
            gt = c.guard_type.value if hasattr(c.guard_type, 'value') else str(c.guard_type)
            lines.append(f"{gt} [{c.key}]: {c.observed_weight:.4f} / {c.limit_weight:.4f} -> BREACHED ({c.message})")

    if not any(c.breached for c in report.checks):
        lines.append("All concentration limits OK.")

    if report.warnings:
        lines.append("Warnings:")
        for w in report.warnings:
            lines.append(f"  - {w}")
    return "\n".join(lines)
