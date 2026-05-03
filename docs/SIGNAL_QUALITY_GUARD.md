# Signal Quality Guard

## Overview
The Signal Quality Guard processes scored signals through a set of rejection checks and validation rules to ensure only valid, adequately reasoned, and safe signals are pushed through for human review or (in future phases) trade execution.

## Rejection Reasons
The quality guard might assign `SignalQualityStatus.REJECTED` under any of the following conditions (`SignalRejectionReason`):
- `LOW_CONFIDENCE`: The score-calibrated confidence falls below the configuration threshold.
- `LOW_SCORE`: The overall score falls beneath the configuration threshold.
- `MISSING_REASONS`: The signal provided absolutely no string reasons to justify its action.
- `MISSING_FEATURE_SNAPSHOT`: The signal did not attach its driving features.
- `EXPIRED_SIGNAL`: The signal specifies an expiration datetime that has already passed in UTC.

## Overconfidence Warning
As the bot runs completely without a Backtest Engine during this phase, any signal generating an exceedingly high confidence value (>0.80) will be logged with a `WARNING` status or penalized heavily in scoring to prevent overly optimistic filtering.

**Note:** Quality filtering is exclusively an assessment and validation layer, and it does not serve as a risk engine executing or omitting real trade orders.

## CLI Usage Example

```bash
# Validate rules and verify rejection rates across signal inputs
python -m usa_signal_bot signal-quality-check --file data/signals/example_signals.jsonl
```
