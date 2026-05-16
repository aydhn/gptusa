from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioConstructionReview
from typing import Any

def attach_portfolio_construction_to_walk_forward_result(result: dict[str, Any], reviews_by_window: dict[str, PortfolioConstructionReview] | None = None) -> dict[str, Any]:
    res = dict(result)
    res["portfolio_construction"] = {}
    if reviews_by_window:
        for w, r in reviews_by_window.items():
            if r.plan and r.plan.exposure_snapshot:
                res["portfolio_construction"][w] = {
                    "gross": r.plan.exposure_snapshot.gross_exposure_usd,
                    "net": r.plan.exposure_snapshot.net_exposure_usd
                }
    return res

def walk_forward_portfolio_construction_summary(result: dict[str, Any]) -> dict[str, Any]:
    return result.get("portfolio_construction", {})

def walk_forward_exposure_stability(result: dict[str, Any]) -> dict[str, Any]:
    pc = result.get("portfolio_construction", {})
    if not pc: return {"stability": "UNKNOWN"}
    grosses = [v.get("gross", 0) for v in pc.values()]
    if not grosses: return {"stability": "UNKNOWN"}

    max_g = max(grosses)
    min_g = min(grosses)
    return {
        "stability": "STABLE" if (max_g - min_g) / (max_g + 1) < 0.2 else "UNSTABLE",
        "max_gross": max_g,
        "min_gross": min_g
    }

def walk_forward_portfolio_construction_warnings(result: dict[str, Any]) -> list[str]:
    stab = walk_forward_exposure_stability(result)
    if stab.get("stability") == "UNSTABLE":
        return ["Walk-forward portfolio exposure is unstable across windows."]
    return []
