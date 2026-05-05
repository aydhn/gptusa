# Sensitivity Limitations

While the parameter sensitivity and robustness map features provide invaluable context into a strategy's behavior, they carry several inherent limitations that must be understood.

## 1. No Future Guarantee
Robust parameters on historical data do NOT guarantee profitability on out-of-sample or live data. The stability map purely represents historical landscape topography.

## 2. Grid Range Assumptions
The results are constrained entirely by the grid ranges defined by the user. If the user only explores extremely tight intervals, the "stability" score will artificially inflate.

## 3. Survivorship Bias
The signal datasets applied during backtesting rely on the underlying universe snapshot. If the universe does not historically correct for survivorship bias (e.g., delisted stocks), the sensitivity metrics will skew positively.

## 4. Feature Leakage
If the generated signals rely on indicators that leak future data or repaint, the backtest results will be overly optimistic. Sensitivity scores will not detect feature leakage; they will merely show "stable" success based on bad data.

## 5. Not an Optimizer
This system is intentionally stripped of any "optimization" routines. It will never output `best_params` or auto-update configuration files.
