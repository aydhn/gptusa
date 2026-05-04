# Walk-Forward Analysis Foundation

This document describes the foundation for Walk-Forward Analysis in the USA Signal Bot project, introduced in Phase 28.

## Overview
Walk-Forward Analysis is a backtesting methodology that continuously moves a training window and a testing window forward in time. This simulates how a strategy would have performed if it were deployed in real-time, periodically re-evaluating its decisions on new out-of-sample data.

**Crucially, in Phase 28, there is NO parameter optimization or machine learning.** The system performs an **evaluation only**, splitting your existing historical signals or candidates into In-Sample (IS) and Out-Of-Sample (OOS) segments to evaluate consistency.

## Capabilities
- Supports **Rolling**, **Anchored**, and **Expanding** modes.
- Aggregates performance metrics across all OOS windows.
- Calculates OOS positive window ratios and degradation versus IS performance.
- Automatically generates validation reports to ensure strict adherence to historical simulation.

## Limitations & Disclaimers
Walk-forward analysis results do not guarantee future performance. See `WALK_FORWARD_LIMITATIONS.md` for a full list of disclaimers.

## CLI Commands

To view the configuration:
```bash
python -m usa_signal_bot walk-forward-info
```

To plan windows:
```bash
python -m usa_signal_bot walk-forward-plan --start 2022-01-01 --end 2025-01-01
```

To run an analysis on previously generated signals:
```bash
python -m usa_signal_bot walk-forward-run-signals --signal-file data/signals/example.jsonl --symbols AAPL,MSFT --timeframe 1d --write
```
