# Runtime Regression Alerting

A deterministic alerting engine that tracks shifts between the latest execution sample and historical `p90` baselines.

## Detection Logic
When a drift (`BETTER`, `WORSE`, `MIXED`) is observed via the comparison delta, it translates into a categorical status mapping:
- `NO_REGRESSION`
- `MINOR_REGRESSION`
- `MODERATE_REGRESSION` (Triggers `WARN`)
- `MAJOR_REGRESSION` (Triggers `FAIL`)
- `CRITICAL_REGRESSION` (Triggers `BLOCK`)

## Alert Rules
Rules match incoming comparisons to configured minimum severity thresholds. Alerts generated strictly write to `data/performance/alerts/` or standard output.

**Important**:
- `Telegram Real Send` is explicitly toggled `OFF` for performance notifications natively to protect API limits.
- No rule generated signals broker actions.

## CLI Usage

Generate Reports:
```bash
python -m usa_signal_bot runtime-regression-check --write
```

Dry-Run Local Telegram Preview:
```bash
python -m usa_signal_bot performance-notification-preview --latest-review
```
