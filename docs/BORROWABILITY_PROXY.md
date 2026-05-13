# Borrowability Proxy

Estimates the realism of shorting a given symbol based on liquidity, price level, and lifecycle risks.

## Components
- **Borrowability Status**: `LIKELY_EASY`, `LIKELY_NORMAL`, `LIKELY_HARD`, `LIKELY_UNAVAILABLE`, `REVIEW_REQUIRED`
- **Short Realism Guard**: Blocks `BLOCK_SIGNAL` or sets to `REVIEW_REQUIRED` based on proxy availability.

## Example Usage
```bash
python -m usa_signal_bot borrowability-proxy --symbol SPY
python -m usa_signal_bot short-realism-check --symbol SPY
```

*Note: This is a purely local heuristic proxy. It is NOT connected to real locate or borrow feeds.*
