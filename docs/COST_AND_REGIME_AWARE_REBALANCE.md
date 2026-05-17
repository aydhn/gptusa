# Cost and Regime Aware Rebalancing

Rebalance thresholds scale dynamically.

- **High Transaction Cost:** Actions are suppressed, or thresholds are increased.
- **High Market Impact:** Suppresses non-critical additions.
- **High Transition Risk / Risk-Off:** Regime throttles block new entries and increases.
- **High Drawdown:** Drastic reduction in allowed risk additions, preferring risk-reducing exits.

## CLI Usage
`python -m usa_signal_bot turnover-cost --delta-notional 1000 --cost-bps 50`
`python -m usa_signal_bot rebalance-thresholds`
