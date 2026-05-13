# Corporate Action Guard

## Overview
Detects and warns about stock splits, dividends, and anomalous price gaps.

## Purpose
Prevents running backtests or executing signals immediately following unadjusted price jumps that resemble severe corporate actions. Emits local guard metadata (`BLOCK_SIGNAL`, `WATCH`).

## Disclaimer
Outputs from this guard are heuristically calculated and do not constitute formal investment advice or trading halts.

## CLI
`python -m usa_signal_bot corporate-actions-info`
`python -m usa_signal_bot split-detect --symbol AAPL`
`python -m usa_signal_bot corporate-action-guard --symbol AAPL`
