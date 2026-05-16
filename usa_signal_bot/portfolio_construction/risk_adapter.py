from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioConstructionPlan
from typing import Any

def portfolio_construction_risk_summary(plan: PortfolioConstructionPlan) -> dict[str, Any]:
    if not plan.exposure_snapshot: return {}
    return {
        "gross_exposure_usd": plan.exposure_snapshot.gross_exposure_usd,
        "net_exposure_usd": plan.exposure_snapshot.net_exposure_usd,
        "long_exposure_usd": plan.exposure_snapshot.long_exposure_usd,
        "short_exposure_usd": plan.exposure_snapshot.short_exposure_usd,
        "concentration_assessments": len(plan.concentration_assessments),
        "blocked_allocations": plan.blocked_count + plan.suppressed_count
    }

def portfolio_construction_risk_warnings(plan: PortfolioConstructionPlan) -> list[str]:
    warns = []
    for a in plan.concentration_assessments:
        warns.extend(a.warnings)
    return warns

def attach_portfolio_construction_to_risk_report(report: dict[str, Any], plan: PortfolioConstructionPlan) -> dict[str, Any]:
    res = dict(report)
    res["portfolio_risk"] = portfolio_construction_risk_summary(plan)
    res["portfolio_warnings"] = portfolio_construction_risk_warnings(plan)
    return res

def risk_adapter_summary_to_text(payload: dict[str, Any]) -> str:
    risk = payload.get("portfolio_risk", {})
    return f"Portfolio Risk: Gross ${risk.get('gross_exposure_usd', 0):.2f}, Blocked: {risk.get('blocked_allocations', 0)}"
