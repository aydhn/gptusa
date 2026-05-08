# Paper Drawdown Monitoring

The Paper Drawdown Monitoring module tracks the equity curve of virtual accounts to identify drops from peak equity. This module serves as a simulated risk tracking mechanism purely for research and evaluation purposes.

## Key Concepts
- **Max Drawdown**: The largest peak-to-trough percentage drop in the paper account.
- **Current Drawdown**: The current percentage drop from the highest peak achieved so far.
- **Thresholds**: Defined in the configuration for `warning`, `breach`, and `critical` drawdown limits.
- **Drawdown Events**: Generated when the drawdown percentage crosses one of the predefined thresholds.

> **Important:** A drawdown warning or breach does NOT issue any real or paper orders to stop-loss or close positions. It exists only to emit a report and potentially trigger a notification for review.

## Example CLI Usage
To check the latest drawdown report locally:
```bash
python -m usa_signal_bot paper-drawdown-report --latest-paper --write
```
