# Exposure Guard

The Exposure Guard acts as the portfolio-wide risk tracker, preventing concentration risk and overextension.

## Purpose
It maintains an `ExposureSnapshot` containing data on available cash, total exposure, open positions, and exposure distribution. **The Exposure Guard does not generate broker orders; it operates purely as an analytical guardrail.**

## Tracked Metrics
- **Portfolio Exposure**: The total allocated notional vs. equity.
- **Symbol Exposure**: Maximum allowed allocation toward a single underlying symbol.
- **Strategy Exposure**: Maximum allocation allowed for a specific strategy algorithm.
- **Timeframe Exposure**: (Tracked, but limit enforcement is optional) The concentration of trades on specific intervals.
- **Cash Buffer**: Rejects sizing that dips cash levels below a safety reserve.
- **Max Open Positions**: Cap on the absolute number of distinct instruments held.
- **Short Disabled by Default**: By default, shorting action requests trigger a rejection unless explicitly allowed via the `allow_short` parameter.

## CLI Reporting
Check the latest run's evaluated snapshot metrics:
`python -m usa_signal_bot risk-latest`
