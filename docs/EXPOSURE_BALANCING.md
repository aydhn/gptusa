# Exposure Balancing

The Exposure Balancing layer calculates portfolio snapshots based on theoretical candidates or current allocations.

## Types of Exposure
- **Gross Exposure**: Absolute sum of all notional values.
- **Net Exposure**: Sum of long (+ve) and short (-ve) notionals.
- **Long/Short Exposure**: Absolute sums of specific sides.

Limits can be configured to `WARNING`, `REDUCE`, or `BLOCK` allocations that push the portfolio past defined bounds.

## Example CLI Commands
```bash
python -m usa_signal_bot exposure-snapshot --equity 100000
python -m usa_signal_bot exposure-limits --equity 100000
```
