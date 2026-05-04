# Transaction Cost Models

The USA Signal Bot engine provides a customizable, simulated transaction cost modeling layer for backtesting purposes.

**Important:** These models are rough estimates for backtesting only. They do not guarantee or perfectly mirror real-world execution costs from any specific broker. The backtest engine does not connect to live brokers.

## Available Models

- **NONE**: Zero fees are applied.
- **FLAT_FEE**: A fixed flat fee is applied per trade fill regardless of quantity or notional value.
- **BPS (Basis Points)**: Fee is calculated as a percentage of the total notional value of the trade fill. `1 bps = 0.01%`.
- **PER_SHARE**: A fixed fee amount is applied per share/contract in the fill.
- **COMBINED**: A combination of flat fee, bps, and per-share models.

## Configuration Parameters

- `model_type`: The type of model to use.
- `flat_fee`: Fixed fee amount (e.g., $1.00).
- `fee_bps`: Basis points to charge on the notional value.
- `per_share_fee`: Fee charged per unit of quantity.
- `min_fee`: A floor applied to the final calculated fee.
- `max_fee`: A ceiling applied to the final calculated fee.

## Effective Fee BPS

The system calculates an `effective_fee_bps` for reporting purposes. This shows the final fee charged as a percentage of the notional value in basis points, making it easy to compare costs across different models.

## CLI Usage

You can view the current configuration using:

```bash
python -m usa_signal_bot backtest-cost-info
```

During an advanced backtest run, you can override the BPS fee using the `--fee-bps` argument:

```bash
python -m usa_signal_bot backtest-run-signals-advanced --signal-file data/signals/example.jsonl --symbols AAPL --timeframe 1d --fee-bps 2.0
```
