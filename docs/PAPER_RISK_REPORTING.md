# Paper Risk Reporting

The Paper Risk Reporting module evaluates the virtual account's positions, cash balance, and equity against a set of predefined local risk limits. It ensures the simulation remains within expected research boundaries.

## Risk Limits Checked
- **Drawdown Limits**: Max and current drawdown against warning/breach thresholds.
- **Exposure to Equity**: Ensures the total exposure is not excessively high relative to total equity.
- **Cash Buffer**: Checks if the available cash is above the minimum required percentage.
- **Open Positions**: Validates the total number of simultaneous open positions.
- **Largest Position Weight**: Checks if any single position represents too large a percentage of the total equity.

## Output
The report categorizes the account's risk level into `LOW`, `MODERATE`, `HIGH`, or `CRITICAL` based on whether the checks passed, warned, or breached limits.

> **Note:** This is purely a dashboard-free text/json report. It is not a real portfolio risk report and should not be used as financial advice.

## Example CLI Usage
```bash
python -m usa_signal_bot paper-risk-report --latest-paper --write
```
