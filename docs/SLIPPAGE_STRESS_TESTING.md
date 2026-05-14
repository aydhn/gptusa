
# Slippage Stress Testing

## Purpose
Simulates specific degradation in execution prices (slippage) to see if a strategy remains profitable.

## Modifiers
- Slippage Multipliers (e.g., 1.5x, 2.0x, 3.0x).
- Fill Realism Modes (Baseline, Conservative, Pessimistic, Strict).

## Warning
These tests are heuristics and do not replace real order book data.

## CLI Commands
`python -m usa_signal_bot slippage-stress --base-bps 20`
`python -m usa_signal_bot fill-realism-stress`
