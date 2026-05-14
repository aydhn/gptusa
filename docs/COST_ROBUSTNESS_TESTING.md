
# Cost Robustness Testing

## Purpose
Cost Robustness Testing evaluates how well a strategy's returns hold up when transaction costs are significantly worse than the baseline assumptions.

## Scenarios
- **Baseline**: 1.0x multipliers.
- **Mild**: 1.25x slippage/spread/impact.
- **Moderate**: 1.5x slippage/spread/impact, 1.25x fee.
- **Severe**: 2.0x slippage/spread/impact, 1.5x fee.
- **Extreme**: 3.0x slippage/spread/impact, 2.0x fee, Strict Fill Realism.

## Outputs
Gross vs. Stressed Net results, Failed Scenario counts, and a Cost Robustness Score.

## CLI Commands
`python -m usa_signal_bot cost-robustness-info`
`python -m usa_signal_bot cost-stress-scenarios`
`python -m usa_signal_bot cost-robustness-review --write`
