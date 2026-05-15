from typing import Any
import numpy as np
from usa_signal_bot.regime_map.regime_map_models import MultiTimeframeRegimeConfirmation

def cross_sectional_return_dispersion(symbol_rows: dict[str, list[dict[str, Any]]], lookback: int = 20) -> float | None:
    if not symbol_rows or len(symbol_rows) < 5:
        return None

    returns = []
    for symbol, rows in symbol_rows.items():
        if len(rows) > lookback:
            current = rows[-1]['close']
            past = rows[-lookback-1]['close']
            if past > 0:
                returns.append((current - past) / past)

    if not returns:
        return None

    # Standard deviation of returns across the universe is a proxy for dispersion
    return float(np.std(returns) * 100) # Percentage

def cross_sectional_volatility_dispersion(confirmations: list[MultiTimeframeRegimeConfirmation]) -> float | None:
    if not confirmations or len(confirmations) < 5:
        return None

    vols = []
    for c in confirmations:
        # Get daily realized vol if available
        for snap in c.snapshots:
            if snap.timeframe.value == 'DAILY':
                vol = snap.evidence.get('volatility', {}).get('realized_volatility_annualized')
                if vol is not None:
                    vols.append(vol)
                break

    if not vols:
        return None

    return float(np.std(vols))

def sector_proxy_dispersion(symbol_metadata: dict[str, dict[str, Any]] | None, confirmations: list[MultiTimeframeRegimeConfirmation]) -> dict[str, Any]:
    # Placeholder for sector dispersion if metadata is provided
    # In absence of paid API, we might not have sector data, so return empty or basic metrics
    if not symbol_metadata:
        return {"reason": "No sector metadata available"}

    # Logic to group by sector and compute dispersion would go here
    return {"status": "Not implemented without sector data"}

def dispersion_score(confirmations: list[MultiTimeframeRegimeConfirmation], symbol_rows: dict[str, list[dict[str, Any]]] | None = None) -> float | None:
    # A normalized score 0-100 indicating how dispersed the market is
    # Higher dispersion = more rotation / less broad trend
    vol_disp = cross_sectional_volatility_dispersion(confirmations)

    if vol_disp is None:
        return None

    # Heuristic normalization: vol std dev of > 20% across universe is very high
    score = (vol_disp / 20.0) * 100
    return min(max(score, 0.0), 100.0)

def dispersion_proxy_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Dispersion Score: {summary.get('dispersion_score', 0.0):.1f}"
