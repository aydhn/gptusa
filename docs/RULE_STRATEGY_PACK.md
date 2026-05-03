# Rule Strategy Pack

Rule strategies are organized into "Sets" for easy execution via CLI.

## Strategy Sets

- `basic_rules`: Trend and Momentum.
- `trend_rules`: Trend Following + Volume Confirmation.
- `momentum_rules`: Momentum Continuation + Volume Confirmation.
- `mean_reversion_rules`: Mean Reversion.
- `breakout_rules`: Volatility Breakout + Volume Confirmation.
- `full_rules`: All standard rule strategies + Composite.

## CLI Usage

View details about a set and its required features:
```bash
python -m usa_signal_bot rule-strategy-set-info --set full_rules
```

Run an entire set and generate a Confluence Report:
```bash
python -m usa_signal_bot rule-strategy-run-set --set basic_rules --symbols AAPL,MSFT --timeframes 1d --write
```
