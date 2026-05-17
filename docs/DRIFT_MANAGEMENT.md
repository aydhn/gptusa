# Drift Management

## Drift Types
- **Symbol Drift:** Absolute percentage weight difference for a single ticker.
- **Exposure Drift:** Gross, Net, Long, Short drift vs targets.
- **Bucket Drift:** Sector, Cluster, Strategy, Regime, Cost, and Liquidity bucket limits vs current state.
- **Signal Decay Drift:** Evaluates time-based validity of signals forming the target allocations.

## CLI Usage
`python -m usa_signal_bot drift-summary --equity 100000`
`python -m usa_signal_bot bucket-drift --equity 100000`
`python -m usa_signal_bot signal-decay --age-minutes 120`
