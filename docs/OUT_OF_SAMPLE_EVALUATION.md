# Out-of-Sample (OOS) Evaluation

Out-of-sample evaluation assesses how well signals perform on data that was not used during the original strategy generation or training period.

## Core Metrics
- **OOS Positive Window Ratio**: The percentage of test windows that yielded a positive return. E.g., if 8 out of 10 windows are profitable, the ratio is 0.8.
- **Average OOS Return**: The mean return across all out-of-sample windows.
- **Average Degradation**: Measures how much the performance degraded from In-Sample to Out-of-Sample (OOS Return - IS Return). A negative value indicates that OOS performed worse than IS.
- **Stability Score**: A normalized score (0-100) combining the OOS positive ratio and penalizing significant degradation.

## Result Buckets
Runs are automatically classified based on these metrics:
- **OOS Classification**: STRONG, ACCEPTABLE, WEAK, FAILED, INSUFFICIENT_DATA.
- **Stability Bucket**: STABLE, MODERATE, UNSTABLE, SEVERELY_UNSTABLE.

*Note: High stability or STRONG classification does not guarantee live market profitability.*
