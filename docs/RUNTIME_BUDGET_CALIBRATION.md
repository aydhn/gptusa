# Runtime Budget Calibration

This documentation covers Phase 49's runtime budget evaluation algorithms.

## Purpose
The Runtime Budget Calibration system assesses historical `ResourceProfile` data bounds against deterministic percentiles to establish safe operational limits for subsequent operations (Backtests, Rehearsals, Scans).

## Mechanics
* **Percentile Approximations**: Collects memory peaks and wall-time distributions from `data/profiling/profiles/*.json`. Generates suggestions dynamically scaling up budgets around the `p75` and `p90` windows if sufficient sample counts exist.
* **Confidence Scoring**: Demands a minimum number of completed profiles per scope before recommending aggressive throttling behavior. Without enough samples, the system opts for `INSUFFICIENT_DATA` combined with `REVIEW_REQUIRED`.

## Available Decisions
* `KEEP_CURRENT`: Maintain existing bounds.
* `RAISE_BUDGET`: The limits appear too restrictive given recent historical data.
* `LOWER_BUDGET`: The system consistently operates well below stated maximums.
* `SPLIT_TASK` or `THROTTLE_TASK`: Tasks consistently struggle within logical capacity.
* `REVIEW_REQUIRED`: Default fallback or low-confidence boundary.

## CLI Usage

Run runtime budget calibration evaluation manually:
```bash
python -m usa_signal_bot budget-calibrate --write
python -m usa_signal_bot calibration-latest
```

*Note: Budget Calibration output operates strictly locally and does not constitute investment advice.*
