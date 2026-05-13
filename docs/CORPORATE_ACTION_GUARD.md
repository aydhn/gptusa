# Corporate Action Guard

**DISCLAIMER: NOT INVESTMENT ADVICE. NO BROKER/LIVE EXECUTION.**
Detects gaps, splits, and dividend irregularities locally. Emits metadata warnings (e.g. `BLOCK_SIGNAL`) to prevent distorted feature computation.
Heuristic detections are not guaranteed to be perfectly accurate.

## Usage
`python -m usa_signal_bot corporate-actions-info`
`python -m usa_signal_bot split-detect --symbol AAPL`
`python -m usa_signal_bot corporate-action-guard --symbol AAPL`
