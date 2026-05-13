# Universe Survivorship-Bias Guard

## Overview
Survivorship bias is a critical risk in quantitative research where historical backtests inadvertently use a modern (current) universe of active symbols, completely missing symbols that were delisted, acquired, or went bankrupt during the test period. This artificially inflates returns by only looking at the "survivors".

The **Survivorship-Bias Guard** subsystem provides local, evidence-based alerts and validation gates to protect against this bias.

## Key Mechanisms
1. **Universe Snapshot Tracking:** Allows the system to freeze universe memberships over time (`HISTORICAL`, `CURRENT`) and validate the exact symbol list used in backtests against a historical point in time.
2. **Current vs. Historical Backtest Guard:** If a historical backtest is initiated using only current universe snapshots (without historical evidence), the guard will attach a `HIGH` risk warning.
3. **Delisting Evidence Processing:** By analyzing missing histories and registry data, the guard identifies delisted stocks to assess overall universe health.

## Guard Status & Risk Levels
- **Risk Levels:** `NONE`, `LOW`, `MODERATE`, `HIGH`, `CRITICAL`
- **Guard Status:**
  - `CLEAR`: No survivorship bias indicators detected.
  - `WARNING`: Current universe vs. historical mismatch or incomplete metadata.
  - `REVIEW_REQUIRED`: Substantial unknowns in the symbol list.
  - `BLOCK_BACKTEST`: (Optional) Block execution if CRITICAL risks exist.
  - `BLOCK_SIGNAL`: Active scan hitting a delisted symbol.

## CLI Usage
Assess survivorship risk for a given historical window:
```bash
python -m usa_signal_bot survivorship-review --write
```
Run a full universe lifecycle report:
```bash
python -m usa_signal_bot universe-lifecycle-review --write
```

## Important Disclaimer
A `PASS` or `CLEAR` status from this guard is an **internal research quality metric**. It does not constitute approval for live trading, broker execution, or financial investment advice.
