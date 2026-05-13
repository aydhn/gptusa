# Liquidity and Tradability Guard

The Liquidity and Tradability Guard evaluates symbol historical data to construct a `LiquidityProfile` (ADV, Price Level, Stale Data). It restricts backtests and paper trades on highly illiquid names to prevent unrealistic execution scenarios.

## Components
- **Liquidity Profile**: Computes volume ratios, price levels, and stale data gaps.
- **Tradability Status**: `TRADABLE`, `CAUTION`, `REVIEW_REQUIRED`, `BLOCK_SIGNAL`

## Example Usage
```bash
python -m usa_signal_bot liquidity-profile --symbol SPY
python -m usa_signal_bot tradability-guard --symbol SPY --side long
```

*Note: The guards use purely heuristic proxies. No actual broker order is executed.*
