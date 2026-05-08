# Golden Sample Run

## Overview
A Golden Sample dataset consists of deterministically generated OHLCV bars, along with static signals, candidates, risk decisions, and allocations. It ensures the local software pipeline can execute predictably without needing live data.

## Features
- **Deterministic OHLCV Fixture**: Synthetic OHLCV rows built from a fixed seed. No `yfinance` or internet access is needed.
- **Signal / Candidate / Risk Fixtures**: Synthetic artifacts allowing individual steps to be mocked or isolated.
- **Baseline Snapshots**: Artifact results are hashed into `_baseline.json` files. Use `--update-baseline` to explicitly accept changes.

## Important Note
Golden samples are NOT real market data. They are structurally coherent, synthetic arrays designed purely to execute the local Python code safely.

## CLI Examples

```bash
python -m usa_signal_bot golden-create
python -m usa_signal_bot golden-validate
python -m usa_signal_bot golden-snapshot-summary
```
