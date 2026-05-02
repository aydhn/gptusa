# Signal Quality Guard

## Overview
The Signal Quality Guard acts as a hard filter before any signal is evaluated for paper trading or real execution. It strictly enforces validation thresholds, ensuring that poorly constructed or fundamentally weak signals are immediately rejected.

## Rejection Reasons
Signals can be rejected for multiple reasons, which are tracked via the `SignalRejectionReason` enum:
- `LOW_CONFIDENCE`: The internal model confidence is below the allowable minimum.
- `LOW_SCORE`: The structural signal score is below the minimum threshold.
- `MISSING_REASONS`: The signal lacks explanatory textual reasons.
- `MISSING_FEATURE_SNAPSHOT`: The signal lacks the snapshot of features that led to its creation.
- `DUPLICATE_SIGNAL`: Exact duplicate of an already evaluated signal.
- `CONFLICTING_SIGNAL`: Immediately conflicts with existing high-confidence signals.
- `HIGH_RISK_FLAGS`: Metadata indicates poor data quality or low liquidity.
- `OVERCONFIDENT_WITHOUT_BACKTEST`: Very high confidence without historical backtest support.
- `EXPIRED_SIGNAL`: The evaluation timestamp is outdated.
- `INVALID_SIGNAL`: The signal structurally fails contract validation.

## Quality Reports
The system outputs a detailed `SignalQualityReport` containing `ACCEPTED`, `REJECTED`, `WARNING`, and `NEEDS_REVIEW` metrics.

> **Note:** The quality guard is a validation tool, not a risk engine. It does not look at portfolio allocation, maximum drawdown, or active trades.

## Example CLI Usage

Run a quality check on a generated signal file:
```bash
python -m usa_signal_bot signal-quality-check --file data/signals/example.jsonl
```
