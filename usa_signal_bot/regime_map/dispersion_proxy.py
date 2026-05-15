from typing import Any
import numpy as np

from usa_signal_bot.regime_map.regime_map_models import MultiTimeframeRegimeConfirmation

def cross_sectional_return_dispersion(symbol_rows: dict[str, list[dict[str, Any]]], lookback: int = 20) -> float | None:
    if not symbol_rows:
        return None

    returns = []
    for sym, rows in symbol_rows.items():
        if len(rows) < lookback + 1:
            continue
        current = rows[-1]["close"]
        past = rows[-(lookback + 1)]["close"]
        if past > 0:
            returns.append((current - past) / past)

    if not returns or len(returns) < 5:
        return None

    return float(np.std(returns) * 100) # Dispersion of returns

def cross_sectional_volatility_dispersion(confirmations: list[MultiTimeframeRegimeConfirmation]) -> float | None:
    if not confirmations:
        return None

    vols = []
    for c in confirmations:
        for s in c.snapshots:
            if s.timeframe.value == "DAILY":
                v = s.evidence.get("volatility", {}).get("realized_vol_pct")
                if v is not None:
                     vols.append(v)
                break

    if not vols or len(vols) < 5:
        return None

    return float(np.std(vols))

def sector_proxy_dispersion(symbol_metadata: dict[str, dict[str, Any]] | None, confirmations: list[MultiTimeframeRegimeConfirmation]) -> dict[str, Any]:
    if not symbol_metadata or not confirmations:
        return {"warning": "No sector metadata"}

    sectors = {}
    for c in confirmations:
        sec = symbol_metadata.get(c.symbol, {}).get("sector", "UNKNOWN")
        if sec not in sectors:
            sectors[sec] = []
        sectors[sec].append(c)

    sector_scores = {}
    for sec, confs in sectors.items():
         from usa_signal_bot.regime_map.breadth_proxy import calculate_breadth_score
         sc = calculate_breadth_score(confs)
         if sc is not None:
             sector_scores[sec] = sc

    if not sector_scores:
        return {"warning": "Not enough data per sector"}

    vals = list(sector_scores.values())
    disp = float(np.std(vals))

    return {
        "sector_scores": sector_scores,
        "sector_dispersion": disp
    }

def dispersion_score(confirmations: list[MultiTimeframeRegimeConfirmation], symbol_rows: dict[str, list[dict[str, Any]]] | None = None) -> float | None:
    if not symbol_rows:
        return cross_sectional_volatility_dispersion(confirmations)

    ret_disp = cross_sectional_return_dispersion(symbol_rows)
    if ret_disp is None:
        return cross_sectional_volatility_dispersion(confirmations)

    # Cap score
    return min(100.0, ret_disp * 5)

def dispersion_proxy_summary_to_text(summary: dict[str, Any]) -> str:
    # simple formatting
    text = "Dispersion Proxy Summary:\n"
    for k,v in summary.items():
        text += f"{k}: {v}\n"
    return text
